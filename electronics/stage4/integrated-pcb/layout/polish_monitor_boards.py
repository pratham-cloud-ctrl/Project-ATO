"""Set useful functional/connector silk labels without changing routing."""
import argparse
from pathlib import Path
import re
import pcbnew as pcb

HERE=Path(__file__).resolve().parent
PKG=HERE.parent
LABELS={
    'ADC':'RAW ADC', 'INPUTS':'ANALOG TAPS', 'REFERENCE':'ADC REFERENCE',
    'COMPANION':'ISOLATED COMPANION', 'HEALTH':'HEALTH OBSERVATIONS',
    'HANDOFF':'CHARGE ENDPOINTS', 'ROOT 2':'HOST INTERFACES',
    'MONITORING TRANSPORT':'POWER / ADC PORTS',
    'CHANNEL0':'SOURCE 0 MONITOR', 'CHANNEL1':'SOURCE 1 MONITOR',
    'MONITORING CELL':'POWER / HOST INTERFACES', 'INTEGRATION TAPS':'REFERENCE TAP',
}


def main(name):
    path=PKG/'boards'/name/(name.replace('-','_')+'.kicad_pcb')
    board=pcb.LoadBoard(str(path));changed=[]
    for text in board.GetDrawings():
        if not isinstance(text,pcb.PCB_TEXT):continue
        original=text.GetText()
        key=re.sub(r'\.KICAD[ _]SCH$', '', original)
        if key in LABELS and original!=LABELS[key]:
            text.SetText(LABELS[key]);changed.append((original,LABELS[key]))
    layers=pcb.LSET();layers.AddLayer(pcb.F_CrtYd)
    for fp in board.GetFootprints():
        if not fp.GetReference().startswith('J'):continue
        bb=fp.GetLayerBoundingBox(layers)
        reference=fp.Reference();reference.SetLayer(pcb.F_SilkS);reference.SetVisible(True)
        reference.SetTextAngle(pcb.EDA_ANGLE(0,pcb.DEGREES_T))
        reference.SetTextSize(pcb.VECTOR2I(pcb.FromMM(.9),pcb.FromMM(.9)))
        reference.SetTextThickness(pcb.FromMM(.1))
        reference.SetPosition(pcb.VECTOR2I(bb.GetCenter().x,bb.GetTop()-pcb.FromMM(.7)))
    pcb.SaveBoard(str(path),board)
    print(name,'functional labels',changed,'connector reference silk enabled')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--board',action='append',required=True)
    for name in p.parse_args().board:main(name)
