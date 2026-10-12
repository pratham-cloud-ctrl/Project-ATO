"""Refresh artifact hashes from staged Git blobs without changing environment records.

Stage the intended files first, run this command, then stage manifest.sha256.
Verify with scripts/verify_manifest.py --index before committing.
"""
from pathlib import Path
import hashlib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'provenance/manifest.sha256'


def main():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0')
    names = [name for name in names if name and name != MANIFEST]
    if any('\n' in name or '\r' in name for name in names):
        raise ValueError('Manifest paths must contain no newlines')
    rows = []
    with subprocess.Popen(['git', 'cat-file', '--batch'], cwd=ROOT,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
        for name in names:
            process.stdin.write((':'+name+'\n').encode('utf-8'))
            process.stdin.flush()
            header = process.stdout.readline().decode('ascii').strip()
            if header.endswith(' missing'):
                raise ValueError('Missing staged blob: '+name)
            identity, kind, count = header.split()
            if kind != 'blob':
                raise ValueError('Only regular Git blobs are supported: '+name)
            digest = hashlib.sha256()
            remaining = int(count)
            while remaining:
                chunk = process.stdout.read(min(remaining, 1024*1024))
                if not chunk:
                    raise RuntimeError('Incomplete Git blob: '+name)
                digest.update(chunk)
                remaining -= len(chunk)
            if process.stdout.read(1) != b'\n':
                raise RuntimeError('Malformed Git batch separator')
            rows.append(digest.hexdigest()+'  '+name)
        process.stdin.close()
        if process.wait() != 0:
            raise RuntimeError('Git blob reader failed')
    (ROOT/MANIFEST).write_text('\n'.join(rows)+'\n', encoding='utf-8')
    print(f'{len(rows)} staged Git blob checksums recorded; environment records preserved.')


if __name__ == '__main__':
    main()
