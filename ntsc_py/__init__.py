"""the NTSC graphical filter / shader package."""
from .nes_ntsc import NES_NTSC
from .snes_ntsc import SNES_NTSC
from .sms_ntsc import SMS_NTSC
from .color import NES_PALETTE, rgb2nes, nes2rgb
from .color import rgb32_888_to_rgb16_565, rgb16_565_to_rgb32_888


# explicitly define the outward facing API of the package
__all__ = [
    'NES_PALETTE',
    NES_NTSC.__name__,
    SNES_NTSC.__name__,
    SMS_NTSC.__name__,
    nes2rgb.__name__,
    rgb2nes.__name__,
    rgb16_565_to_rgb32_888.__name__,
    rgb32_888_to_rgb16_565.__name__,
]
