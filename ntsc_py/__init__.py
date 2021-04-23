"""the NTSC package."""
from . import nes_ntsc
from .nes_ntsc import NES_NTSC

# explicitly define the outward facing API of the package
__all__ = [
    nes_ntsc.__name__,
    NES_NTSC.__name__,
]
