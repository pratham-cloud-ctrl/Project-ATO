"""A native geometry receipt must verify on both Windows and Linux checkouts."""
from pathlib import Path
import importlib.util
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('artifact_hashes',Path(__file__).resolve().parents[1]/'scripts/artifact_hashes.py')
hashes=importlib.util.module_from_spec(spec);spec.loader.exec_module(hashes)


class PortableReceiptTests(unittest.TestCase):
    def test_line_endings_and_object_layout_do_not_hide_changed_geometry(self):
        with tempfile.TemporaryDirectory() as directory:
            windows=Path(directory)/'windows.json';linux=Path(directory)/'linux.json'
            windows.write_bytes(b'{\r\n  "parts": [1, 2],\r\n  "volume": 100.0\r\n}\r\n')
            linux.write_bytes(b'{"volume":100.0,"parts":[1,2]}\n')
            self.assertEqual(hashes.canonical_json_digest(windows),hashes.canonical_json_digest(linux))
            linux.write_bytes(b'{"volume":101.0,"parts":[1,2]}\n')
            self.assertNotEqual(hashes.canonical_json_digest(windows),hashes.canonical_json_digest(linux))
            linux.write_bytes(b'{"volume":100.0,"parts":[2,1]}\n')
            self.assertNotEqual(hashes.canonical_json_digest(windows),hashes.canonical_json_digest(linux))


if __name__=='__main__':unittest.main()
