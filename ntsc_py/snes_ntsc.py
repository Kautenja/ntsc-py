"""A CTypes interface to Blargg's C++ SNES NTSC filter."""
import ctypes
import glob
import os
import numpy as np
from .utility import ndarray_from_byte_buffer


# the absolute path to the C++ shared object library
LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'lib_ntsc*')
# load the library from the shared object file
try:
    LIBRARY = ctypes.cdll.LoadLibrary(glob.glob(LIBRARY_PATH)[0])
except IndexError:
    raise OSError('missing static lib_ntsc*.so library!')


# setup the argument and return types for SNES_NTSC_HEIGHT
LIBRARY.SNES_NTSC_HEIGHT.argtypes = None
LIBRARY.SNES_NTSC_HEIGHT.restype = ctypes.c_uint
# setup the argument and return types for SNES_NTSC_WIDTH_INPUT
LIBRARY.SNES_NTSC_WIDTH_INPUT.argtypes = None
LIBRARY.SNES_NTSC_WIDTH_INPUT.restype = ctypes.c_uint
# setup the argument and return types for SNES_NTSC_WIDTH_OUTPUT
LIBRARY.SNES_NTSC_WIDTH_OUTPUT.argtypes = None
LIBRARY.SNES_NTSC_WIDTH_OUTPUT.restype = ctypes.c_uint
# setup the argument and return types for SNES_NTSC_PITCH
LIBRARY.SNES_NTSC_PITCH.argtypes = None
LIBRARY.SNES_NTSC_PITCH.restype = ctypes.c_uint


class snes_ntsc_t(ctypes.Structure):
    """A reference to the `snes_ntsc_setup_t` structure in C."""
    _fields_ = [
        ("table", ctypes.c_void_p),
    ]


# setup the argument and return types for SNES_NTSC_InitializeConfiguration
LIBRARY.SNES_NTSC_InitializeConfiguration.argtypes = None
LIBRARY.SNES_NTSC_InitializeConfiguration.restype = ctypes.POINTER(snes_ntsc_t)
# setup the argument and return types for SNES_NTSC_DestroyConfiguration
LIBRARY.SNES_NTSC_DestroyConfiguration.argtypes = [ctypes.POINTER(snes_ntsc_t)]
LIBRARY.SNES_NTSC_DestroyConfiguration.restype = None


class snes_ntsc_setup_t(ctypes.Structure):
    """A reference to the `snes_ntsc_setup_t` structure in C."""
    _fields_ = [
        ("hue", ctypes.c_double),
        ("saturation", ctypes.c_double),
        ("contrast", ctypes.c_double),
        ("brightness", ctypes.c_double),
        ("sharpness", ctypes.c_double),
        ("gamma", ctypes.c_double),
        ("resolution", ctypes.c_double),
        ("artifacts", ctypes.c_double),
        ("fringing", ctypes.c_double),
        ("bleed", ctypes.c_double),
        ("merge_fields", ctypes.c_int),
        ("decoder_matrix", ctypes.c_void_p),
        ("bsnes_colortbl", ctypes.c_void_p),
    ]


# setup the argument and return types for SNES_NTSC_InitializeSetup
LIBRARY.SNES_NTSC_InitializeSetup.argtypes = None
LIBRARY.SNES_NTSC_InitializeSetup.restype = ctypes.POINTER(snes_ntsc_setup_t)
# setup the argument and return types for SNES_NTSC_DestroySetup
LIBRARY.SNES_NTSC_DestroySetup.argtypes = [ctypes.POINTER(snes_ntsc_setup_t)]
LIBRARY.SNES_NTSC_DestroySetup.restype = None
# setup the argument and return types for SNES_NTSC_SetupComposite
LIBRARY.SNES_NTSC_SetupComposite.argtypes = [ctypes.POINTER(snes_ntsc_setup_t)]
LIBRARY.SNES_NTSC_SetupComposite.restype = None
# setup the argument and return types for SNES_NTSC_SetupSVideo
LIBRARY.SNES_NTSC_SetupSVideo.argtypes = [ctypes.POINTER(snes_ntsc_setup_t)]
LIBRARY.SNES_NTSC_SetupSVideo.restype = None
# setup the argument and return types for SNES_NTSC_SetupRGB
LIBRARY.SNES_NTSC_SetupRGB.argtypes = [ctypes.POINTER(snes_ntsc_setup_t)]
LIBRARY.SNES_NTSC_SetupRGB.restype = None
# setup the argument and return types for SNES_NTSC_SetupMonochrome
LIBRARY.SNES_NTSC_SetupMonochrome.argtypes = [ctypes.POINTER(snes_ntsc_setup_t)]
LIBRARY.SNES_NTSC_SetupMonochrome.restype = None


# setup the argument and return types for SNES_NTSC_InitializeInputPixels
LIBRARY.SNES_NTSC_InitializeInputPixels.argtypes = None
LIBRARY.SNES_NTSC_InitializeInputPixels.restype = ctypes.c_void_p
# setup the argument and return types for SNES_NTSC_DestroyInputPixels
LIBRARY.SNES_NTSC_DestroyInputPixels.argtypes = [ctypes.c_void_p]
LIBRARY.SNES_NTSC_DestroyInputPixels.restype = None


# setup the argument and return types for SNES_NTSC_InitializeOutputPixels
LIBRARY.SNES_NTSC_InitializeOutputPixels.argtypes = None
LIBRARY.SNES_NTSC_InitializeOutputPixels.restype = ctypes.c_void_p
# setup the argument and return types for SNES_NTSC_DestroyOutputPixels
LIBRARY.SNES_NTSC_DestroyOutputPixels.argtypes = [ctypes.c_void_p]
LIBRARY.SNES_NTSC_DestroyOutputPixels.restype = None


# setup the argument and return types for SNES_NTSC_Process
LIBRARY.SNES_NTSC_Process.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(snes_ntsc_t), ctypes.c_bool]
LIBRARY.SNES_NTSC_Process.restype = None


def rgb32_888_to_rgb16_565(img):
    """
    Convert the 32-bit RGB888 image to 16-bit RGB565.

    Args:
        img: the 32-bit image in HWC format and RGB888 color space

    Returns:
        the 16-bit image in HWC format in RGB565 color space

    """
    r = ((32 * img[..., 0:1] / 255).round().astype('uint16') & 0b11111)  << 11
    g = ((64 * img[..., 1:2] / 255).round().astype('uint16') & 0b111111) << 5
    b =  (32 * img[..., 2:3] / 255).round().astype('uint16') & 0b11111
    return r + g + b


def rgb16_565_to_rgb32_888(img):
    """
    Convert the 16-bit RGB565 image to 32-bit RGB888.

    Args:
        img: the 32-bit image in HWC format and RGB565 color space

    Returns:
        the 32-bit image in HWC format in RGB888 color space

    """
    r = (255.0 * ((img >> 11) & 0b11111)  / 32.0).round().astype('uint8')
    g = (255.0 * ((img >> 5)  & 0b111111) / 64.0).round().astype('uint8')
    b = (255.0 * ((img)       & 0b11111)  / 32.0).round().astype('uint8')
    return np.concatenate([r, g, b], axis=-1)


class SNES_NTSC:
    """A graphical filter that models the NTSC Nintendo Entertainment System."""

    def __init__(self, mode='rgb', flicker=True, **kwargs):
        """
        Initialize a new NES NTSC graphical filter.

        Args:
            mode: the video mode to initialize the filter with
            flicker: whether to flicker between renders
            **kwargs: the keyword arguments to pass to the setup structure

        Returns:
            None

        """
        # create the configuration structure that holds the options
        self._config = LIBRARY.SNES_NTSC_InitializeConfiguration()
        self._setup = LIBRARY.SNES_NTSC_InitializeSetup()
        self._input = LIBRARY.SNES_NTSC_InitializeInputPixels()
        self._output = LIBRARY.SNES_NTSC_InitializeOutputPixels()
        # create the input and output buffers
        shape_input = LIBRARY.SNES_NTSC_HEIGHT(), LIBRARY.SNES_NTSC_WIDTH_INPUT(), 1
        self.snes_pixels = ndarray_from_byte_buffer(self._input, shape_input, ctype=ctypes.c_uint16, dtype='uint16')
        shape_output = LIBRARY.SNES_NTSC_HEIGHT(), LIBRARY.SNES_NTSC_WIDTH_OUTPUT(), 4
        self.ntsc_pixels = ndarray_from_byte_buffer(self._output, shape_output)[:, :, 1:]
        # setup the flicker effect
        self.flicker = flicker
        self._is_even_frame = False
        # setup the mode
        self.setup(mode=mode, **kwargs)

    def __del__(self):
        """Delete an instance of NES NTSC."""
        LIBRARY.SNES_NTSC_DestroyConfiguration(self._config)
        LIBRARY.SNES_NTSC_DestroySetup(self._setup)
        LIBRARY.SNES_NTSC_DestroyInputPixels(self._input)
        LIBRARY.SNES_NTSC_DestroyOutputPixels(self._output)

    def setup(self, mode=None, **kwargs):
        """
        Setup the filter.

        Args:
            mode: the base mode to start with if any
            kwargs: the kwargs of the snes_ntsc_setup_t structure to set

        Returns:
            None

        """
        # the preset modes to start with
        MODES = {
            'composite':  LIBRARY.SNES_NTSC_SetupComposite,
            'svideo':     LIBRARY.SNES_NTSC_SetupSVideo,
            'rgb':        LIBRARY.SNES_NTSC_SetupRGB,
            'monochrome': LIBRARY.SNES_NTSC_SetupMonochrome,
        }
        if mode is not None:  # a preset mode was specified
            if mode not in MODES:  # the mode is invalid
                raise ValueError(f'received invalid mode: {repr(mode)}, should be one of {set(MODES.keys())}')
            # lookup the mode setter and call it
            MODES[mode](self._setup)
        # iterate over the setup keyword arguments to set
        for kwarg, value in kwargs.items():
            setattr(self._setup[0], kwarg, value)
        # apply the setup to the configuration
        LIBRARY.SNES_NTSC_SetupApply(self._config, self._setup)

    def process(self):
        """Process the input pixels."""
        if self.flicker:  # flip the even frame accumulator if flickering
            self._is_even_frame = not self._is_even_frame
        LIBRARY.SNES_NTSC_Process(self._output, self._input, self._config, self._is_even_frame)


# explicitly define the outward facing API of this module
__all__ = [SNES_NTSC.__name__]
