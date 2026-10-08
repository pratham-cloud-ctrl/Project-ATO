"""Portable semantic receipt hashes; Git manifests separately bind exact blobs."""
from pathlib import Path
import hashlib
import json


def canonical_json_digest(path):
    """Bind all parsed JSON values/order, independent of text layout/newlines.

    Sorted object keys, preserved array order, compact separators, ASCII JSON
    and finite numbers define the serialized bytes used by this receipt.
    """
    values=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    encoded=json.dumps(values,sort_keys=True,separators=(',',':'),
                       ensure_ascii=True,allow_nan=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()
