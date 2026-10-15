"""Small, explicit copper repairs; native DRC remains the acceptance authority."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import pcbnew as pcb
from build_boards import PKG,mm

def router_split():
    name='contact-router';path=PKG/'boards'/name/'contact_router.kicad_pcb'
    system=json.loads((PKG/'integration/system.json').read_text());comps={c['reference']:c for c in system['components'] if c['board']==name}
    b=pcb.LoadBoard(str(path));mapping=defaultdict(set)
    for f in b.GetFootprints():
        if f.GetReference() not in comps:continue
        pins={p['number']:p['net'] for p in comps[f.GetReference()]['pins']}
        for p in f.Pads():
            if p.GetNumber() in pins:mapping[p.GetNetname()].add(pins[p.GetNumber()])
    split={old for old,new in mapping.items() if len(new)>1}
    removed=[]
    for t in list(b.GetTracks()):
        if t.GetNetname() in split:removed.append(t.m_Uuid.AsString());b.RemoveNative(t)
    for f in b.GetFootprints():
        if f.GetReference() not in comps:continue
        pins={p['number']:p['net'] for p in comps[f.GetReference()]['pins']}
        for p in f.Pads():
            if p.GetNumber() in pins:
                n=b.FindNet(pins[p.GetNumber()])
                if not n:
                    n=pcb.NETINFO_ITEM(b,pins[p.GetNumber()],len(list(b.GetNetsByNetcode()))+1);b.Add(n)
                p.SetNet(n)
    pcb.SaveBoard(str(path),b)
    pcb.ExportSpecctraDSN(b,str(path.with_name('contact_router_corrected.dsn')))
    (path.parent/'split-repair.json').write_text(json.dumps({'split_nets':sorted(split),'removed_copper_items':len(removed),'why':'Original carrier harness return mapping was corrected before final pin graph freeze; old merged GND/SHIFT_TAIL copper must be removed before exact pad reassignment.'},indent=2)+'\n')
    print('removed',len(removed),'split',split)

def remove_dangling(name):
    directory=PKG/'boards'/name;path=directory/(name.replace('-','_')+'.kicad_pcb')
    d=json.loads((directory/'drc.json').read_text());uuids={x['items'][0]['uuid'] for x in d['violations'] if x['type']=='via_dangling'}
    b=pcb.LoadBoard(str(path));removed=[]
    for t in list(b.GetTracks()):
        if t.m_Uuid.AsString() in uuids:b.RemoveNative(t);removed.append(t.m_Uuid.AsString())
    pcb.SaveBoard(str(path),b);print('Removed exact native DRC dangling vias:',len(removed))
    (directory/'removed-dangling-vias.json').write_text(json.dumps({'source_drc_count':len(uuids),'removed':removed},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--router-split',action='store_true');p.add_argument('--remove-dangling');a=p.parse_args()
    if a.router_split:router_split()
    if a.remove_dangling:remove_dangling(a.remove_dangling)
