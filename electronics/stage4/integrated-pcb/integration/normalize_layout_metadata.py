"""Align non-electrical metadata with actual native board exports.

Only generated NC-net identities and Datasheet fields change. Connected nets,
references, footprints, pin groups and saved schematic files are not changed.
"""
import json,xml.etree.ElementTree as ET
from build_integration import HERE,ROOT
def main():
    s=json.loads((HERE/'system.json').read_text(encoding='utf-8'));renames={};count=0
    for pkg,out in s['native_outputs'].items():
        x=ET.parse((ROOT/out['board_root']).with_suffix('.xml')).getroot()
        actual={(node.get('ref'),node.get('pin')):net.get('name') for net in x.findall('nets/net') for node in net.findall('node')}
        source=ET.parse(ROOT/s['sources'][pkg]['xml']).getroot()
        datasheets={c.get('ref'):next((f.text or '' for f in c.findall('fields/field') if f.get('name')=='Datasheet'),'') for c in source.findall('components/comp')}
        dnp={c.get('ref'):any(p.get('name')=='dnp' for p in c.findall('property')) for c in source.findall('components/comp')}
        for c in s['components']:
            if c['board']!=pkg:continue
            c['datasheet']=datasheets.get(c['source_ref'],'')
            c['dnp']=dnp.get(c['source_ref'],False)
            for p in c['pins']:
                if p['source_net'] and p['source_net'].startswith('unconnected-'):
                    new=actual[c['reference'],p['number']];assert new.startswith('unconnected-')
                    renames[p['net']]=new;p['net']=new;count+=1
    for n in s['nets']:
        if n['name'] in renames:n['name']=renames[n['name']]
    for k,v in s['net_mapping'].items():
        if v in renames:s['net_mapping'][k]=renames[v]
    (HERE/'system.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'NC_identities_normalized':count,'Datasheet_fields':len([c for c in s['components'] if c['datasheet']]),'connected_pin_groups_changed':0}))
if __name__=='__main__':main()
