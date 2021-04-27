"""A CTypes interface to Blargg's C++ NES NTSC filter."""
import ctypes
from ._library import LIBRARY
from .utility import ndarray_from_byte_buffer


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


class NES_NTSC:
    """A graphical filter that models the Nintendo Entertainment System."""

    def __init__(self, mode='rgb', flicker=False, **kwargs):
        """
        Initialize a new NES NES_NTSC graphical filter.

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
        self.input = ndarray_from_byte_buffer(self._input, shape_input)
        shape_output = LIBRARY.NES_NTSC_HEIGHT(), LIBRARY.NES_NTSC_WIDTH_OUTPUT(), 4
        self.output = ndarray_from_byte_buffer(self._output, shape_output)[:, :, 1:]
        # setup the flicker effect
        self.flicker = flicker
        self._is_even_frame = False
        # setup the mode
        self.setup(mode=mode, **kwargs)

    def __del__(self):
        """Delete an instance of NES_NTSC."""
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
__all__ = [NES_NTSC.__name__]
