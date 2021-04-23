"""The ctypes library for the project."""
import ctypes
import glob
import os


# the absolute path to the C++ shared object library
LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'lib_ntsc*')
# load the library from the shared object file
try:
    LIBRARY = ctypes.cdll.LoadLibrary(glob.glob(LIBRARY_PATH)[0])
except IndexError:
    raise OSError('missing static lib_ntsc*.so library!')


# explicitly define the outward facing API of this module
__all__ = ['LIBRARY']
