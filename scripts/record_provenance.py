"""Capture environment and hash committed source/export assets; omit host paths."""
from pathlib import Path
import platform,json,hashlib,subprocess
from importlib.metadata import version
ROOT=Path(__file__).resolve().parents[1]
env={'python':platform.python_version(),'platform':platform.system(),'machine':platform.machine(),
     'packages':{p:version(p) for p in ('numpy','matplotlib','reportlab','Pillow','pypdf')},
     'cad_generator':'build123d 0.13.0','blender':'5.2.2 LTS','kicad':'10.0.6',
     'freecad':'1.1.4','ngspice':'46; bundled with KiCad',
     'media_encoder':'imageio-ffmpeg 0.6.0 / bundled FFmpeg',
     'c_compiler':'Zig 0.15.2 C frontend','release_date':'2026-10-07',
     'manifest_content':'SHA-256 of Git-index blob bytes, including Git LF normalization; manifest excludes itself'}
(ROOT/'provenance/environment.json').write_text(json.dumps(env,indent=2))
files=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
files=[name for name in files if name!='provenance/manifest.sha256']
data=subprocess.check_output(['git','cat-file','--batch'],input=('\n'.join(':'+f for f in files)+'\n').encode(),cwd=ROOT)
lines=[];offset=0
for name in files:
    end=data.index(b'\n',offset);header=data[offset:end].decode();size=int(header.rsplit(' ',1)[1])
    contents=data[end+1:end+1+size];offset=end+size+2
    lines.append(hashlib.sha256(contents).hexdigest()+'  '+name)
(ROOT/'provenance/manifest.sha256').write_text('\n'.join(lines)+'\n')
print(len(lines),'artifact hashes recorded.')
