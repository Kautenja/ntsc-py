"""the NTSC graphical filter / shader package."""
from .nes_ntsc import NES_NTSC, rgb2nes, nes2rgb
from .snes_ntsc import SNES_NTSC, rgb32_888_to_rgb16_565, rgb16_565_to_rgb32_888


# explicitly define the outward facing API of the package
__all__ = [
    NES_NTSC.__name__,
    SNES_NTSC.__name__,
    nes2rgb.__name__,
    rgb2nes.__name__,
    rgb16_565_to_rgb32_888.__name__,
    rgb32_888_to_rgb16_565.__name__,
]
