"""Utility methods used in the project."""
import sys
import ctypes
import numpy as np


def ndarray_from_byte_buffer(pointer, shape):
    """
    Create an ndarray wrapper around a buffer of bytes.

    Args:
        pointer: the pointer to the ctypes buffer of bytes to wrap
        shape: the shape that describes the arrangement of the bytes

    Returns:
        an ndarray wrapper around the ctype buffer of bytes

    """
    # create a buffer from the contents of the address location
    raw = ctypes.cast(pointer, ctypes.POINTER(ctypes.c_byte * np.prod(shape))).contents
    # create a NumPy array from the buffer
    pixels = np.frombuffer(raw, dtype=np.uint8)
    # reshape the pixels from a column vector to a tensor
    pixels = pixels.reshape(shape)
    # flip the bytes if the machine is little-endian
    if sys.byteorder == 'little':
        pixels = pixels[..., ::-1]
    return pixels


# explicitly define the outward facing API of this module
__all__ = [ndarray_from_byte_buffer.__name__]
