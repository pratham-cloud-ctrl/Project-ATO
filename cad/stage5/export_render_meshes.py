"""Tessellate saved engineering BReps for reproducible presentation renders.

The mesh is a derivative. Native FreeCAD/STEP and independent fit receipts
remain the engineering authority. Run with FreeCAD Python after generation.
"""
from pathlib import Path
import gzip
import json
import FreeCAD as App
import MeshPart

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'tmp/stage5-render-meshes.json.gz'


def mesh(shape):
    m=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.25,AngularDeflection=.3,Relative=False)
    points,faces=m.Topology
    return dict(vertices=[[round(p.x,5),round(p.y,5),round(p.z,5)] for p in points],faces=faces)


def main():
    result={}
    ref=json.loads((HERE/'reference/contract.json').read_text())
    doc=App.openDocument(str(ROOT/ref['native']))
    records=[]
    for row in ref['parts']:
        obj=doc.getObject(row.get('native_name',row['label']))
        assert obj and not obj.Shape.isNull(),row
        color=list(obj.DisplayColor)[:3] if 'DisplayColor' in obj.PropertiesList else [.2,.3,.4]
        category=row['category']
        board=next((b for b in ref['boards'] if b['label']==row['label']),None)
        # Preserve all source solids, add categorical material rather than
        # painting entire populated assemblies like empty PCB slabs.
        solids=list(obj.Shape.Solids) if board else [obj.Shape]
        for i,s in enumerate(solids):
            c=color
            if board:
                bb=s.BoundBox;z=board['translation_mm'][2]
                if bb.XLength>70 and bb.YLength>70 and bb.ZLength<2:
                    c=[.025,.28,.20]
                elif bb.ZMin<z or (bb.XLength<1.0 or bb.YLength<1.0):
                    c=[.58,.61,.62]
                else:c=[.055,.065,.075]
            record=dict(name=row['label']+(f'_{i:04}' if board else ''),category=category,color=c,mesh=mesh(s))
            record['parent']=row['label']
            if board:record['tier']=board['tier']
            record['explode_z']=ref['exploded_transforms'].get(row['label'],[0,0,0])[2]
            records.append(record)
    App.closeDocument(doc.Name)
    h=json.loads((HERE/'harness/contract.json').read_text())
    doc=App.openDocument(str(ROOT/h['native']))
    hr=json.loads((HERE/'harness/geometry-receipt.json').read_text())
    for row in hr['parts']:
        obj=doc.getObject(row['label'])
        mate=next((m for m in h['mates'] if m['label']==row['label']),None)
        dz=ref['exploded_transforms']['PCB_'+mate['board'].replace('-','_')][2] if mate else 0
        records.append(dict(name=row['label'],parent=row['label'],category='harness_mate',color=list(obj.RenderColour)[:3],mesh=mesh(obj.Shape),explode_z=dz))
    App.closeDocument(doc.Name)
    result['reference']=records
    future=json.loads((HERE/'future-interface/contract.json').read_text())
    future_native=HERE/'future-interface'/future['artifacts']['native']
    doc=App.openDocument(str(future_native))
    records=[]
    for row in future['parts']:
        obj=doc.getObject(row.get('native_name',row.get('name',row['label'])))
        if not obj:obj=next(o for o in doc.Objects if o.Label==row['label'])
        color=row.get('color_rgb',list(obj.DisplayColor)[:3] if 'DisplayColor' in obj.PropertiesList else [.4,.45,.5])
        records.append(dict(name=obj.Name,parent=obj.Label,category=row.get('category','future'),color=color,mesh=mesh(obj.Shape),row=row,explode_translation_mm=future['exploded_transforms'].get(obj.Name,[0,0,0])))
    App.closeDocument(doc.Name)
    result['future']=records
    OUT.parent.mkdir(exist_ok=True)
    with gzip.open(OUT,'wt',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print('Tessellated saved BReps:',{k:len(v) for k,v in result.items()})


if __name__=='__main__':main()
