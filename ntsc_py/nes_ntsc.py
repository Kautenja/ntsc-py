"""A CTypes interface to the C++ NES environment."""
import ctypes
import glob
import os
import numpy as np
from .utility import ndarray_from_byte_buffer


# the absolute path to the C++ shared object library
LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'ntsc/lib_ntsc*')
# load the library from the shared object file
try:
    LIBRARY = ctypes.cdll.LoadLibrary(glob.glob(LIBRARY_PATH)[0])
except IndexError:
    raise OSError('missing static lib_ntsc_env*.so library!')


# setup the argument and return types for NES_NTSC_HEIGHT
LIBRARY.NES_NTSC_HEIGHT.argtypes = None
LIBRARY.NES_NTSC_HEIGHT.restype = ctypes.c_uint
# setup the argument and return types for NES_NTSC_WIDTH_INPUT
LIBRARY.NES_NTSC_WIDTH_INPUT.argtypes = None
LIBRARY.NES_NTSC_WIDTH_INPUT.restype = ctypes.c_uint
# setup the argument and return types for NES_NTSC_WIDTH_OUTPUT
LIBRARY.NES_NTSC_WIDTH_OUTPUT.argtypes = None
LIBRARY.NES_NTSC_WIDTH_OUTPUT.restype = ctypes.c_uint
# setup the argument and return types for NES_NTSC_PITCH
LIBRARY.NES_NTSC_PITCH.argtypes = None
LIBRARY.NES_NTSC_PITCH.restype = ctypes.c_uint


class nes_ntsc_t(ctypes.Structure):
    """A reference to the `nes_ntsc_setup_t` structure in C."""
    _fields_ = [
        ("table", ctypes.c_void_p),
    ]


# setup the argument and return types for NES_NTSC_InitializeConfiguration
LIBRARY.NES_NTSC_InitializeConfiguration.argtypes = None
LIBRARY.NES_NTSC_InitializeConfiguration.restype = ctypes.POINTER(nes_ntsc_t)
# setup the argument and return types for NES_NTSC_DestroyConfiguration
LIBRARY.NES_NTSC_DestroyConfiguration.argtypes = [ctypes.POINTER(nes_ntsc_t)]
LIBRARY.NES_NTSC_DestroyConfiguration.restype = None


class nes_ntsc_setup_t(ctypes.Structure):
    """A reference to the `nes_ntsc_setup_t` structure in C."""
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
        ("palette_out", ctypes.c_void_p),
        ("palette", ctypes.c_void_p),
        ("base_palette", ctypes.c_void_p),
    ]


# setup the argument and return types for NES_NTSC_InitializeSetup
LIBRARY.NES_NTSC_InitializeSetup.argtypes = None
LIBRARY.NES_NTSC_InitializeSetup.restype = ctypes.POINTER(nes_ntsc_setup_t)
# setup the argument and return types for NES_NTSC_DestroySetup
LIBRARY.NES_NTSC_DestroySetup.argtypes = [ctypes.POINTER(nes_ntsc_setup_t)]
LIBRARY.NES_NTSC_DestroySetup.restype = None
# setup the argument and return types for NES_NTSC_SetupComposite
LIBRARY.NES_NTSC_SetupComposite.argtypes = [ctypes.POINTER(nes_ntsc_setup_t)]
LIBRARY.NES_NTSC_SetupComposite.restype = None
# setup the argument and return types for NES_NTSC_SetupSVideo
LIBRARY.NES_NTSC_SetupSVideo.argtypes = [ctypes.POINTER(nes_ntsc_setup_t)]
LIBRARY.NES_NTSC_SetupSVideo.restype = None
# setup the argument and return types for NES_NTSC_SetupRGB
LIBRARY.NES_NTSC_SetupRGB.argtypes = [ctypes.POINTER(nes_ntsc_setup_t)]
LIBRARY.NES_NTSC_SetupRGB.restype = None
# setup the argument and return types for NES_NTSC_SetupMonochrome
LIBRARY.NES_NTSC_SetupMonochrome.argtypes = [ctypes.POINTER(nes_ntsc_setup_t)]
LIBRARY.NES_NTSC_SetupMonochrome.restype = None


# setup the argument and return types for NES_NTSC_InitializeInputPixels
LIBRARY.NES_NTSC_InitializeInputPixels.argtypes = None
LIBRARY.NES_NTSC_InitializeInputPixels.restype = ctypes.c_void_p
# setup the argument and return types for NES_NTSC_DestroyInputPixels
LIBRARY.NES_NTSC_DestroyInputPixels.argtypes = [ctypes.c_void_p]
LIBRARY.NES_NTSC_DestroyInputPixels.restype = None


# setup the argument and return types for NES_NTSC_InitializeOutputPixels
LIBRARY.NES_NTSC_InitializeOutputPixels.argtypes = None
LIBRARY.NES_NTSC_InitializeOutputPixels.restype = ctypes.c_void_p
# setup the argument and return types for NES_NTSC_DestroyOutputPixels
LIBRARY.NES_NTSC_DestroyOutputPixels.argtypes = [ctypes.c_void_p]
LIBRARY.NES_NTSC_DestroyOutputPixels.restype = None


# setup the argument and return types for NES_NTSC_Process
LIBRARY.NES_NTSC_Process.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(nes_ntsc_t), ctypes.c_bool]
LIBRARY.NES_NTSC_Process.restype = None


# the color palette for rendering RGB colors
PALETTE = np.array([
    [102,102,102], [  0, 42,136], [ 20, 18,168], [ 59,  0,164],
    [ 92,  0,126], [110,  0, 64], [108,  7,  0], [ 87, 29,  0],
    [ 52, 53,  0], [ 12, 73,  0], [  0, 82,  0], [  0, 79,  8],
    [  0, 64, 78], [  0,  0,  0], [  0,  0,  0], [  0,  0,  0],
    [174,174,174], [ 21, 95,218], [ 66, 64,254], [118, 39,255],
    [161, 27,205], [184, 30,124], [181, 50, 32], [153, 79,  0],
    [108,110,  0], [ 56,135,  0], [ 13,148,  0], [  0,144, 50],
    [  0,124,142], [  0,  0,  0], [  0,  0,  0], [  0,  0,  0],
    [254,254,254], [100,176,254], [147,144,254], [199,119,254],
    [243,106,254], [254,110,205], [254,130,112], [235,159, 35],
    [189,191,  0], [137,217,  0], [ 93,229, 48], [ 69,225,130],
    [ 72,206,223], [ 79, 79, 79], [  0,  0,  0], [  0,  0,  0],
    [254,254,254], [193,224,254], [212,211,254], [233,200,254],
    [251,195,254], [254,197,235], [254,205,198], [247,217,166],
    [229,230,149], [208,240,151], [190,245,171], [180,243,205],
    [181,236,243], [184,184,184], [  0,  0,  0], [  0,  0,  0]
], dtype=np.uint8)


def rgb2nes(img):
    """
    Convert the RGB image to NES palette.

    Args:
        img: the image in HWC format and RGB color space

    Returns:
        a matrix of NES color palette indexes that closely match the RGB colors

    """
    # compute the MSE between the image and each color in the palette
    distance = (img.astype(float) - PALETTE[:, None, None, :].astype(float))**2
    distance = np.mean(distance, axis=-1, keepdims=True)
    # return the color with the lowest error as the code for each RGB tuple
    return np.argmin(distance, axis=0).astype(np.uint8)


def nes2rgb(img):
    """
    Convert the NES palette image to RGB.

    Args:
        img: the image in HW format and NES color space

    Returns:
        a matrix of RGB color tuple that are referenced by the palette

    """
    return PALETTE[img]


class NES_NTSC:
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
        self._config = LIBRARY.NES_NTSC_InitializeConfiguration()
        self._setup = LIBRARY.NES_NTSC_InitializeSetup()
        self._input = LIBRARY.NES_NTSC_InitializeInputPixels()
        self._output = LIBRARY.NES_NTSC_InitializeOutputPixels()
        # create the input and output buffers
        shape_input = LIBRARY.NES_NTSC_HEIGHT(), LIBRARY.NES_NTSC_WIDTH_INPUT(), 1
        self.nes_pixels = ndarray_from_byte_buffer(self._input, shape_input)
        shape_output = LIBRARY.NES_NTSC_HEIGHT(), LIBRARY.NES_NTSC_WIDTH_OUTPUT(), 4
        self.ntsc_pixels = ndarray_from_byte_buffer(self._output, shape_output)[:, :, 1:]
        # setup the flicker effect
        self.flicker = flicker
        self._is_even_frame = False
        # setup the mode
        self.setup(mode=mode, **kwargs)

    def __del__(self):
        """Delete an instance of NES NTSC."""
        LIBRARY.NES_NTSC_DestroyConfiguration(self._config)
        LIBRARY.NES_NTSC_DestroySetup(self._setup)
        LIBRARY.NES_NTSC_DestroyInputPixels(self._input)
        LIBRARY.NES_NTSC_DestroyOutputPixels(self._output)

    def setup(self, mode=None, **kwargs):
        """
        Setup the filter.

        Args:
            mode: the base mode to start with if any
            kwargs: the kwargs of the nes_ntsc_setup_t structure to set

        Returns:
            None

        """
        # the preset modes to start with
        MODES = {
            'composite':  LIBRARY.NES_NTSC_SetupComposite,
            'svideo':     LIBRARY.NES_NTSC_SetupSVideo,
            'rgb':        LIBRARY.NES_NTSC_SetupRGB,
            'monochrome': LIBRARY.NES_NTSC_SetupMonochrome,
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
        LIBRARY.NES_NTSC_SetupApply(self._config, self._setup)

    def process(self):
        """Process the input pixels."""
        if self.flicker:  # flip the even frame accumulator if flickering
            self._is_even_frame = not self._is_even_frame
        LIBRARY.NES_NTSC_Process(self._output, self._input, self._config, self._is_even_frame)


# explicitly define the outward facing API of this module
__all__ = [NES_NTSC.__name__, rgb2nes.__name__, nes2rgb.__name__, 'PALETTE']
