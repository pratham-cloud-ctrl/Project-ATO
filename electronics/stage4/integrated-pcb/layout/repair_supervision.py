"""Finite repair of two actual supervision nets; native DRC remains required."""
import argparse
import json
from pathlib import Path
import pcbnew as pcb
import copper_grid as grid

HERE=Path(__file__).resolve().parent
PATH=HERE.parent/'boards/supervision/supervision.kicad_pcb'


def route(name):
    board=pcb.LoadBoard(str(PATH))
    nets={n.GetNetname():n.GetNetCode() for n in board.GetNetsByNetcode().values()}
    net=nets[name]
    # Both nets are simple two-pin connections. Replacing the complete old
    # copper removes dangling exploratory candidates rather than hiding them.
    copper=[t for t in board.GetTracks() if t.GetNetCode()==net]
    for item in copper:board.Remove(item)
    pins=[pad for fp in board.GetFootprints() for pad in fp.Pads() if pad.GetNetCode()==net]
    assert len(pins)==2,(name,len(pins))
    if name.endswith('WD_CWD'):
        # Route from the actual SMD copper. The grid chooses any layer changes
        # only where its through-via clearance mask allows them; a preselected
        # via location must not punch through an existing inner-layer trace.
        endpoints=[(grid.xy(pad.GetPosition()),[0]) for pad in sorted(pins,key=lambda p:p.GetPosition().x)]
    else:
        # One SMD logic output and one through-hole observation header.
        source=next(p for p in pins if p.GetAttribute()==pcb.PAD_ATTRIB_SMD)
        target=next(p for p in pins if p.GetAttribute()==pcb.PAD_ATTRIB_PTH)
        endpoints=[(grid.xy(source.GetPosition()),[0]),(grid.xy(target.GetPosition()),list(range(4)))]
    blocked,via=grid.obstacles(board,net)
    path,n=grid.route(blocked,via,*endpoints,max_nodes=2000000)
    result=grid.copper(board,net,path,*endpoints)
    pcb.SaveBoard(str(PATH),board)
    print(json.dumps(dict(net=name,expanded_nodes=n,copper=result,removed_old_items=len(copper))),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--net',required=True);a=p.parse_args();route(a.net)
