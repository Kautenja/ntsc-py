"""the NTSC package."""
from .nes_ntsc import NES_NTSC


# explicitly define the outward facing API of the package
__all__ = [NES_NTSC.__name__]
