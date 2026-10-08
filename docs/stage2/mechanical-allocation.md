# Preliminary implant and companion allocations

Stage 2 defines envelopes so acquisition, stimulation, energy and mechanical
work can be developed together. These are editable engineering solids and
reservations, **not the finished implant/lead CAD** promised for Stage 5.

| Allocation | Nominal dimensions | Status |
|---|---|---|
| Core can | 60×48×14 mm, 1.2 mm wall | Chosen enclosure; open body plus separate unsealed lid |
| Header | 60×10×14 mm | Dielectric material/antenna/coil reservation; construction unresolved |
| Complete core envelope | 60×58×14 mm | 48 mm metal can plus external 10 mm header |
| Board | 50×40×1 mm | Flat unpopulated allocation, bottom z=1.8 mm |
| Component zone above board | 50×40×3 mm | Spatial reservation; chosen chip footprints do not imply completed routing |
| HV capacitor bank | 24×14×3 mm | Must later provide33 µF effective capacitance at high bias |
| Battery bounding box | 35.1×17×5.5 mm | Contego200 catalog bounding box; actual cell volume3.05 cm³ differs from box |
| Companion | 100×60×24 mm | Preliminary open housing plus unsealed lid |
| Body interface ports | 36, two rows of18 | Illustrative bores/insulators/pins, no qualified hermetic feedthrough |

The [battery manufacturer](https://resonetics.com/wp-content/uploads/2022/08/15507-01-Battery-Brochure-Contego-200-mAh.pdf)
specifies a negative case. It must be electrically isolated from housing and
body-bias/reference nets. Nominal battery-to-component-zone clearance is0.5 mm;
battery-to-lid clearance is1.0 mm. Neither includes a validated tolerance,
insulation compression, swelling, weld allowance or lead routing. Reopen the
envelope if these require more space.

The STEP assembly contains labelled solid parts. The separate populated-zone
STEP is a **reservation volume**, intentionally containing the capacitor bank;
it is excluded from physical-part interference checks. All major nonreservation
solids are checked for volumetric intersections, and each solid for BRep validity.
Port pitch and coordinate positions are illustrative engineering allocations,
not an anatomical or manufactured connector design. Leads/contact areas and
target-specific anatomical routing will be developed with the selected circuit.

Inspect [the STEP assembly](../../cad/stage2/ATO_stage2_allocation.step),
[the native FreeCAD assembly](../../cad/stage2/ATO_stage2_allocation.FCStd),
[the fit/dimension receipt](../../cad/stage2/allocation-checks.json) and
[the parametric generator](../../cad/stage2/build_envelope.py). The
[explicit FreeCAD launcher](../../cad/stage2/OPEN_STAGE2_CAD.cmd) uses the installed
tool path and avoids Windows file-association ambiguity. From the repo root,
run the generator using a Python environment with build123d0.13:

```powershell
& 'E:\project workspace assests\CAD\build123d\.venv\Scripts\python.exe' cad/stage2/build_envelope.py
& 'E:\project workspace assests\CAD\FreeCAD\bin\python.exe' cad/stage2/assemble_freecad.py
```

The nominal package does not establish anatomical fit, sealing, long-term
materials behavior, strain relief, a populated electronics assembly or inductive/
radio coupling. A titanium-like metal can cannot be assumed transparent to RF;
antenna/coil performance through a separately defined dielectric region needs
field and power analysis. An oversized reserved header is not proof that a coil
fits. Thermal resistance remains an independent unqualified model input.
