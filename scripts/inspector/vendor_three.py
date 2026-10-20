"""Pin a local, MIT-licensed Three.js runtime for the public inspector.

Downloads the npm release tarball over HTTPS, verifies its npm SHA-512 integrity,
and copies only the browser modules used here. No npm lifecycle code is run.
"""
import base64
import hashlib
from io import BytesIO
import json
from pathlib import Path
import tarfile
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
VERSION = '0.186.1'
FILES = ['LICENSE', 'package.json', 'build/three.module.js', 'build/three.core.js',
         'examples/jsm/loaders/GLTFLoader.js', 'examples/jsm/controls/OrbitControls.js',
         'examples/jsm/utils/BufferGeometryUtils.js', 'examples/jsm/utils/SkeletonUtils.js']


def main():
    metadata_url = f'https://registry.npmjs.org/three/{VERSION}'
    with urlopen(metadata_url, timeout=60) as response:
        metadata = json.load(response)
    with urlopen(metadata['dist']['tarball'], timeout=60) as response:
        data = response.read()
    expected = 'sha512-' + base64.b64encode(hashlib.sha512(data).digest()).decode()
    assert expected == metadata['dist']['integrity']
    output = ROOT / 'inspector/vendor/three'
    hashes = {}
    with tarfile.open(fileobj=BytesIO(data), mode='r:gz') as archive:
        for name in FILES:
            member = archive.getmember('package/' + name)
            assert member.isfile()
            payload = archive.extractfile(member).read()
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            hashes[name] = hashlib.sha256(payload).hexdigest()
    (output / 'version.json').write_text(json.dumps({
        'package': 'three', 'version': VERSION, 'license': 'MIT',
        'metadata_url': metadata_url, 'tarball': metadata['dist']['tarball'],
        'integrity': expected, 'files_sha256': hashes,
    }, indent=2) + '\n', encoding='utf-8')
    print('Verified Three.js', VERSION, ':', len(FILES), 'vendored files')


if __name__ == '__main__':
    main()
