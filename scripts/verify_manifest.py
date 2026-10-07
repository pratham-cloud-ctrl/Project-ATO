"""Verify the release's committed Git blobs, independent of checkout line endings.

Run before regenerating study outputs: python scripts/verify_manifest.py
Use --index while preparing a release; default verification reads HEAD.
"""
from pathlib import Path
import argparse
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--index', action='store_true')
args = parser.parse_args()
entries = []
for line in (ROOT / 'provenance/manifest.sha256').read_text().splitlines():
    checksum, name = line.split('  ', 1)
    entries.append((checksum, name))
prefix = ':' if args.index else 'HEAD:'
query = '\n'.join(prefix + name for _, name in entries) + '\n'
data = subprocess.check_output(['git', 'cat-file', '--batch'],
                               input=query.encode(), cwd=ROOT)
offset = 0
for expected, name in entries:
    end = data.index(b'\n', offset)
    header = data[offset:end].decode()
    if header.endswith(' missing'):
        raise AssertionError(f'Missing Git blob: {name}')
    size = int(header.rsplit(' ', 1)[1])
    content = data[end + 1:end + 1 + size]
    offset = end + size + 2
    actual = hashlib.sha256(content).hexdigest()
    assert actual == expected, f'Release checksum mismatch: {name}'
print(f'{len(entries)} Git blob checksums verified.')
