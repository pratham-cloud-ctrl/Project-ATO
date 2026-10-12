"""Small synchronous ngspice shared-library adapter; no binary redistributed.

API: https://ngspice.sourceforge.io/shared.html
Adapted from the project's read-only Stage 3 adapter, without importing its models.
"""
import ctypes as ct
import ctypes.util
import os
from pathlib import Path
import numpy as np

class VectorInfo(ct.Structure):
    _fields_ = [("name", ct.c_char_p), ("type", ct.c_int), ("flags", ct.c_short),
                ("real", ct.POINTER(ct.c_double)), ("complex", ct.c_void_p), ("length", ct.c_int)]

def find_library(requested=None):
    if requested:
        return requested
    if os.environ.get("NGSPICE_LIBRARY"):
        return os.environ["NGSPICE_LIBRARY"]
    candidate = Path(r"E:\project workspace assests\EDA\KiCAD\bin\ngspice.dll")
    if os.name == "nt" and candidate.is_file():
        return str(candidate)
    return ctypes.util.find_library("ngspice")

class SharedNgspice:
    def __init__(self, library):
        self.library = library
        self.dll_directories = []
        if os.name == "nt" and Path(library).is_file():
            self.dll_directories.append(os.add_dll_directory(str(Path(library).parent)))
        self.lib = ct.CDLL(library)
        self.messages = []
        send_char = ct.CFUNCTYPE(ct.c_int, ct.c_char_p, ct.c_int, ct.c_void_p)
        controlled_exit = ct.CFUNCTYPE(ct.c_int, ct.c_int, ct.c_bool, ct.c_bool, ct.c_int, ct.c_void_p)
        send_data = ct.CFUNCTYPE(ct.c_int, ct.c_void_p, ct.c_int, ct.c_int, ct.c_void_p)
        send_init = ct.CFUNCTYPE(ct.c_int, ct.c_void_p, ct.c_int, ct.c_void_p)
        background = ct.CFUNCTYPE(ct.c_int, ct.c_bool, ct.c_int, ct.c_void_p)
        def output(message, *_):
            self.messages.append(message.decode("utf-8", errors="replace"))
            return 0
        def noop(*_):
            return 0
        self.callbacks = [send_char(output), send_char(noop), controlled_exit(noop), send_data(noop), send_init(noop), background(noop)]
        self.lib.ngSpice_Init.argtypes = [send_char, send_char, controlled_exit, send_data, send_init, background, ct.c_void_p]
        self.lib.ngSpice_Init.restype = ct.c_int
        self.lib.ngSpice_Command.argtypes = [ct.c_char_p]
        self.lib.ngSpice_Command.restype = ct.c_int
        self.lib.ngSpice_Circ.argtypes = [ct.POINTER(ct.c_char_p)]
        self.lib.ngSpice_Circ.restype = ct.c_int
        self.lib.ngGet_Vec_Info.argtypes = [ct.c_char_p]
        self.lib.ngGet_Vec_Info.restype = ct.POINTER(VectorInfo)
        if self.lib.ngSpice_Init(*self.callbacks, None):
            raise RuntimeError("ngSpice_Init failed")
        self.command("version")
        self.version_messages = list(self.messages)
    def command(self, command):
        if self.lib.ngSpice_Command(command.encode("ascii")):
            raise RuntimeError("ngspice command failed: " + command)
    def vector(self, name):
        pointer = self.lib.ngGet_Vec_Info(name.encode("ascii"))
        if not pointer or pointer.contents.length <= 0 or not pointer.contents.real:
            raise RuntimeError("ngspice vector missing: " + name)
        info = pointer.contents
        return np.ctypeslib.as_array(info.real, shape=(info.length,)).copy()
    def run(self, lines, vectors):
        self.command("destroy all")
        start = len(self.messages)
        encoded = [line.encode("ascii") for line in lines]
        circuit = (ct.c_char_p * (len(encoded) + 1))(*encoded, None)
        if self.lib.ngSpice_Circ(circuit):
            raise RuntimeError("ngSpice_Circ failed")
        self.command("run")
        data = {name: self.vector(name) for name in ["time"] + vectors}
        if not all(np.isfinite(value).all() for value in data.values()):
            raise RuntimeError("Nonfinite transient vector")
        if any(len(value) != len(data["time"]) for value in data.values()) or not (np.diff(data["time"]) > 0).all():
            raise RuntimeError("Inconsistent transient vectors")
        return data, self.messages[start:]
