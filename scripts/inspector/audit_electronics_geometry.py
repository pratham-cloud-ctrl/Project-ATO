#!/usr/bin/env python3
"""Read-only review of native vector extents and interactive board payloads."""
from __future__ import annotations
import importlib.util
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "inspector"
NS = {"s": "http://www.w3.org/2000/svg"}
spec = importlib.util.spec_from_file_location("ibom_svgpath", SITE / "vendor/ibom/InteractiveHtmlBom/ecad/svgpath.py")
svgpath = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svgpath)


class Logger:
    def warn(self, message):
        raise AssertionError("Unsupported vector segment in geometry audit: " + message)


def bounds(svg):
    root = ET.parse(svg).getroot()
    box = [float(v) for v in root.attrib["viewBox"].split()]
    extent = [float("inf"), float("-inf"), float("inf"), float("-inf")]
    count = 0

    def include(bb):
        nonlocal count
        if bb:
            count += 1
            extent[0] = min(extent[0], bb[0]); extent[1] = max(extent[1], bb[1])
            extent[2] = min(extent[2], bb[2]); extent[3] = max(extent[3], bb[3])

    for item in root.iter():
        trans = item.attrib.get("transform", "")
        tag = item.tag.rsplit("}", 1)[-1]
        attr = item.attrib
        if trans not in {"", "translate(0 0) scale(1 1)"}:
            leaves = [x for x in item.iter() if not list(x)]
            assert all(x.tag.rsplit("}", 1)[-1] == "text" and x.attrib.get("opacity") == "0" for x in leaves), (svg, trans)
        if tag == "path":
            path = attr.get("d", "")
            # Native KiCad's stroke font produces many straight paths. Avoid
            # constructing millions of objects for their simple M/L segments.
            commands = set(re.findall(r"[A-DF-Za-df-z]", path))
            if commands <= {"M", "L", "Z"}:
                pts = re.findall(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?", path)
                assert len(pts) % 2 == 0
                xs, ys = list(map(float, pts[::2])), list(map(float, pts[1::2]))
                if xs:
                    include((min(xs), max(xs), min(ys), max(ys)))
            else:
                for segment in svgpath.parse_path(path, Logger()):
                    include(segment.bbox())
        elif tag == "circle":
            x, y, r = (float(attr[k]) for k in ["cx", "cy", "r"])
            include((x-r, x+r, y-r, y+r))
        elif tag == "rect":
            x, y = float(attr.get("x", 0)), float(attr.get("y", 0))
            include((x, x+float(attr["width"]), y, y+float(attr["height"])))
        elif tag in {"polygon", "polyline"}:
            nums = list(map(float, re.findall(r"[-+]?(?:\d*\.\d+|\d+)", attr["points"])))
            include((min(nums[::2]), max(nums[::2]), min(nums[1::2]), max(nums[1::2])))
        elif tag == "line":
            include((min(float(attr["x1"]), float(attr["x2"])), max(float(attr["x1"]), float(attr["x2"])),
                     min(float(attr["y1"]), float(attr["y2"])), max(float(attr["y1"]), float(attr["y2"]))))
    outside = [max(0, box[0]-extent[0]), max(0, extent[1]-(box[0]+box[2])),
               max(0, box[1]-extent[2]), max(0, extent[3]-(box[1]+box[3]))]
    return {"viewBox": box, "vector_extents_xxyy": extent, "primitives": count, "outside_mm_lrtb": outside}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", action="store_true", help="Also compare every drawn pad's board-space position and net to KiCad's native pcbnew API.")
    args = parser.parse_args()
    if args.native:
        import pcbnew
    manifest = json.loads((SITE / "assets/electronics-manifest.json").read_text(encoding="utf-8"))
    with (ROOT / "electronics/stage4/integrated-pcb/integration/populated-bom.csv").open(encoding="utf-8", newline="") as source:
        component_values = {(row["board"], row["reference"]): row for row in csv.DictReader(source)}
    sheets, copper, boards = [], [], []
    for sheet in manifest["sheets"]:
        result = bounds(SITE / sheet["svg"])
        result.update(id=sheet["id"], page=sheet["page"], file=sheet["svg"])
        assert max(result["outside_mm_lrtb"]) <= 0.5, result
        sheets.append(result)
    for board in manifest["boards"]:
        for layer in board["copper"]:
            result = bounds(SITE / layer["svg"])
            result.update(board=board["id"], layer=layer["id"])
            # Board-edge stroke and the drill/edge cut can extend a fraction
            # of a millimetre beyond the board-area frame.
            assert max(result["outside_mm_lrtb"]) <= 0.5, result
            copper.append(result)
        html = (SITE / board["ibom"]).read_text(encoding="utf-8")
        payload = json.loads(re.search(r"^var pcbdata = (\{.*\})$", html, re.M).group(1))
        assert payload["ibom_version"] == "v2.12.0"
        refmap = {fp["ref"]: fp for fp in payload["footprints"]}
        fitted = {ref for row in payload["bom"]["both"] for ref, idx in row}
        assert len(fitted) == board["fitted"]
        assert not fitted.intersection(board["dnp"])
        assert set(board["dnp"]).issubset(refmap)
        assert all("net" in pad for fp in refmap.values() for pad in fp["pads"])
        assert all(pad["net"] in payload["nets"]
                   for fp in refmap.values() for pad in fp["pads"])
        for group in payload["bom"]["both"]:
            for reference, index in group:
                value, footprint = payload["bom"]["fields"][str(index)]
                original = component_values[(board["id"], reference)]
                assert value == original["value"], (board["id"], reference, value, original["value"])
                assert footprint == original["footprint"].rsplit(":", 1)[-1], (board["id"], reference, footprint, original["footprint"])
        assert all(payload["tracks"][s] and isinstance(payload["zones"][s], list) for s in ["F", "B"])
        if args.native:
            native = pcbnew.LoadBoard(str(ROOT / board["source"]))
            actual_footprints = {f.GetReference(): f for f in native.GetFootprints()}
            assert set(refmap) == set(actual_footprints)
            paste_only_apertures = 0
            for reference, rendered in refmap.items():
                actual = actual_footprints[reference]
                all_pads = list(actual.Pads())
                outer_or_drill = [p for p in all_pads if pcbnew.F_Cu in list(p.GetLayerSet().Seq()) or pcbnew.B_Cu in list(p.GetLayerSet().Seq()) or p.GetAttribute() in [pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH]]
                paste_only_apertures += len(all_pads) - len(outer_or_drill)
                expected = Counter((round(pcbnew.ToMM(p.GetPosition().x), 6), round(pcbnew.ToMM(p.GetPosition().y), 6), p.GetNetname()) for p in outer_or_drill)
                drawn = Counter((round(p["pos"][0], 6), round(p["pos"][1], 6), p["net"]) for p in rendered["pads"])
                assert expected == drawn, (board["id"], reference, expected - drawn, drawn - expected)
                if reference in fitted:
                    assert actual.GetValue() == component_values[(board["id"], reference)]["value"]
                assert rendered["layer"] == ("F" if actual.GetLayer() == pcbnew.F_Cu else "B")
        boards.append({"id": board["id"], "fitted": len(fitted), "drawn_footprints": len(refmap),
                       "native_net_names": len(payload["nets"]), "native_pads": sum(len(fp["pads"]) for fp in refmap.values()),
                       "non_copper_apertures_outside_interactive_copper_scope": paste_only_apertures if args.native else None,
                       "dnp_omitted_from_fitted_bom": board["dnp"], "ibom_version": payload["ibom_version"]})
    print(json.dumps({"status": "pass", "native_pad_position_net_comparison": args.native, "review": "Bounded vector extents and interactive native pad/net payloads; no electrical redesign or qualification.",
                      "schematic_sheets": sheets, "copper_layers": copper, "boards": boards}, indent=2))


if __name__ == "__main__":
    main()
