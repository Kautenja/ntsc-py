"""A CTypes interface to Blargg's C++ SMS NTSC filter."""
import ctypes
from ._library import LIBRARY
from .utility import ndarray_from_byte_buffer


# setup the argument and return types for SMS_NTSC_HEIGHT
LIBRARY.SMS_NTSC_HEIGHT.argtypes = None
LIBRARY.SMS_NTSC_HEIGHT.restype = ctypes.c_uint
# setup the argument and return types for SMS_NTSC_WIDTH_INPUT
LIBRARY.SMS_NTSC_WIDTH_INPUT.argtypes = None
LIBRARY.SMS_NTSC_WIDTH_INPUT.restype = ctypes.c_uint
# setup the argument and return types for SMS_NTSC_WIDTH_OUTPUT
LIBRARY.SMS_NTSC_WIDTH_OUTPUT.argtypes = None
LIBRARY.SMS_NTSC_WIDTH_OUTPUT.restype = ctypes.c_uint
# setup the argument and return types for SMS_NTSC_PITCH
LIBRARY.SMS_NTSC_PITCH.argtypes = None
LIBRARY.SMS_NTSC_PITCH.restype = ctypes.c_uint


class sms_ntsc_t(ctypes.Structure):
    """A reference to the `sms_ntsc_setup_t` structure in C."""
    _fields_ = [
        ("table", ctypes.c_void_p),
    ]


# setup the argument and return types for SMS_NTSC_InitializeConfiguration
LIBRARY.SMS_NTSC_InitializeConfiguration.argtypes = None
LIBRARY.SMS_NTSC_InitializeConfiguration.restype = ctypes.POINTER(sms_ntsc_t)
# setup the argument and return types for SMS_NTSC_DestroyConfiguration
LIBRARY.SMS_NTSC_DestroyConfiguration.argtypes = [ctypes.POINTER(sms_ntsc_t)]
LIBRARY.SMS_NTSC_DestroyConfiguration.restype = None


class sms_ntsc_setup_t(ctypes.Structure):
    """A reference to the `sms_ntsc_setup_t` structure in C."""
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
    ]


# setup the argument and return types for SMS_NTSC_InitializeSetup
LIBRARY.SMS_NTSC_InitializeSetup.argtypes = None
LIBRARY.SMS_NTSC_InitializeSetup.restype = ctypes.POINTER(sms_ntsc_setup_t)
# setup the argument and return types for SMS_NTSC_DestroySetup
LIBRARY.SMS_NTSC_DestroySetup.argtypes = [ctypes.POINTER(sms_ntsc_setup_t)]
LIBRARY.SMS_NTSC_DestroySetup.restype = None
# setup the argument and return types for SMS_NTSC_SetupComposite
LIBRARY.SMS_NTSC_SetupComposite.argtypes = [ctypes.POINTER(sms_ntsc_setup_t)]
LIBRARY.SMS_NTSC_SetupComposite.restype = None
# setup the argument and return types for SMS_NTSC_SetupSVideo
LIBRARY.SMS_NTSC_SetupSVideo.argtypes = [ctypes.POINTER(sms_ntsc_setup_t)]
LIBRARY.SMS_NTSC_SetupSVideo.restype = None
# setup the argument and return types for SMS_NTSC_SetupRGB
LIBRARY.SMS_NTSC_SetupRGB.argtypes = [ctypes.POINTER(sms_ntsc_setup_t)]
LIBRARY.SMS_NTSC_SetupRGB.restype = None
# setup the argument and return types for SMS_NTSC_SetupMonochrome
LIBRARY.SMS_NTSC_SetupMonochrome.argtypes = [ctypes.POINTER(sms_ntsc_setup_t)]
LIBRARY.SMS_NTSC_SetupMonochrome.restype = None


# setup the argument and return types for SMS_NTSC_InitializeInputPixels
LIBRARY.SMS_NTSC_InitializeInputPixels.argtypes = None
LIBRARY.SMS_NTSC_InitializeInputPixels.restype = ctypes.c_void_p
# setup the argument and return types for SMS_NTSC_DestroyInputPixels
LIBRARY.SMS_NTSC_DestroyInputPixels.argtypes = [ctypes.c_void_p]
LIBRARY.SMS_NTSC_DestroyInputPixels.restype = None


# setup the argument and return types for SMS_NTSC_InitializeOutputPixels
LIBRARY.SMS_NTSC_InitializeOutputPixels.argtypes = None
LIBRARY.SMS_NTSC_InitializeOutputPixels.restype = ctypes.c_void_p
# setup the argument and return types for SMS_NTSC_DestroyOutputPixels
LIBRARY.SMS_NTSC_DestroyOutputPixels.argtypes = [ctypes.c_void_p]
LIBRARY.SMS_NTSC_DestroyOutputPixels.restype = None


# setup the argument and return types for SMS_NTSC_Process
LIBRARY.SMS_NTSC_Process.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(sms_ntsc_t)]
LIBRARY.SMS_NTSC_Process.restype = None


class SMS_NTSC:
    """A graphical filter that models the Sega Master System."""

    def __init__(self, mode='rgb', **kwargs):
        """
        Initialize a new SMS_NTSC graphical filter.

        Args:
            mode: the video mode to initialize the filter with
            **kwargs: the keyword arguments to pass to the setup structure

        Returns:
            None

        """
        # create the configuration structure that holds the options
        self._config = LIBRARY.SMS_NTSC_InitializeConfiguration()
        self._setup = LIBRARY.SMS_NTSC_InitializeSetup()
        self._input = LIBRARY.SMS_NTSC_InitializeInputPixels()
        self._output = LIBRARY.SMS_NTSC_InitializeOutputPixels()
        # create the input and output buffers
        shape_input = LIBRARY.SMS_NTSC_HEIGHT(), LIBRARY.SMS_NTSC_WIDTH_INPUT(), 1
        self.input = ndarray_from_byte_buffer(self._input, shape_input,
            ctype=ctypes.c_uint16,
            dtype='uint16'
        )
        shape_output = LIBRARY.SMS_NTSC_HEIGHT(), LIBRARY.SMS_NTSC_WIDTH_OUTPUT(), 4
        self.output = ndarray_from_byte_buffer(self._output, shape_output)[:, :, 1:]
        # setup the mode
        self.setup(mode=mode, **kwargs)

    def __del__(self):
        """Delete an instance of SMS_NTSC."""
        LIBRARY.SMS_NTSC_DestroyConfiguration(self._config)
        LIBRARY.SMS_NTSC_DestroySetup(self._setup)
        LIBRARY.SMS_NTSC_DestroyInputPixels(self._input)
        LIBRARY.SMS_NTSC_DestroyOutputPixels(self._output)

    def setup(self, mode=None, **kwargs):
        """
        Setup the filter.

        Args:
            mode: the base mode to start with if any
            kwargs: the kwargs of the sms_ntsc_setup_t structure to set

        Returns:
            None

        """
        # the preset modes to start with
        MODES = {
            'composite':  LIBRARY.SMS_NTSC_SetupComposite,
            'svideo':     LIBRARY.SMS_NTSC_SetupSVideo,
            'rgb':        LIBRARY.SMS_NTSC_SetupRGB,
            'monochrome': LIBRARY.SMS_NTSC_SetupMonochrome,
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
        LIBRARY.SMS_NTSC_SetupApply(self._config, self._setup)

    def process(self):
        """Process the input pixels."""
        LIBRARY.SMS_NTSC_Process(self._output, self._input, self._config)


# explicitly define the outward facing API of this module
__all__ = [SMS_NTSC.__name__]
