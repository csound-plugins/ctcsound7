import ctypes as ct
import ctypes.util
import sys
from functools import cache
from .common import BUILDING_DOCS


def csoundLibraryName() -> str:
    platform = sys.platform
    if platform.startswith('linux'):
        return 'csound64'
    elif platform.startswith('win'):
        return 'csound64'
    elif platform.startswith('darwin'):
        return 'CsoundLib64'
    else:
        raise RuntimeError(f"Platform '{platform}' not supported")


_libcsound = None
_libcsoundpath = ''


def csoundDLL() -> tuple[ct.CDLL, str]:
    if BUILDING_DOCS:
        raise RuntimeError("Cannot access the dll while building docs")

    global _libcsound
    global _libcsoundpath

    if _libcsound is not None:
        return _libcsound, _libcsoundpath

    if sys.platform == 'linux':
        try:
            dll = ct.CDLL("libcsound64.so")
            _libcsound = dll
            _libcsoundpath = "libcsound64.so"
            return dll, "libcsound64.so"
        except OSError:
            libname = ctypes.util.find_library("csound64")
    else:
        libname = csoundLibraryName()
    path = ctypes.util.find_library(libname)
    if path is None:
        raise ImportError(f"Csound library not found (searched for '{libname}') - Make sure that csound is installed")
    _libcsound = ct.CDLL(path)
    _libcsoundpath = path

    return _libcsound, _libcsoundpath
