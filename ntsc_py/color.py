"""Color-space transformation functions."""
import numpy as np


# the palette for rendering RGB colors on the Nintendo Entertainment System
NES_PALETTE = np.array([
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
    distance = (img.astype(float) - NES_PALETTE[:, None, None, :].astype(float))**2
    distance = np.mean(distance, axis=-1, keepdims=True)
    # return the color with the lowest error as the code for each RGB tuple
    return np.argmin(distance, axis=0).astype(np.uint8)


def nes2rgb(img):
    """
    Convert the NES palette image to RGB.

    Args:
        img: the image in HW or HW1 format in NES color space

    Returns:
        a matrix of RGB color tuple that are referenced by the palette

    """
    if len(img.shape) == 2:  # matrix input, continue
        pass
    elif len(img.shape) == 3 and img.shape[-1] == 1:  # 1 channel 3D input
        img = img[..., 0]  # flatten the outer dimension to a 2D matrix
    else:  # invalid NES pixels
        raise ValueError(
            'expected 2D input or 3D input with 1 channel, '
            f'but received input with shape {repr(img.shape)}'
        )
    return NES_PALETTE[img]


def rgb32_888_to_rgb16_565(img):
    """
    Convert the 32-bit RGB888 image to 16-bit RGB565.

    Args:
        img: the 32-bit image in HWC format and RGB888 color space

    Returns:
        the 16-bit image in HWC format in RGB565 color space

    """
    r = ((32 * img[..., 0:1] / 255).round().astype(np.uint16) & 0b11111)  << 11
    g = ((64 * img[..., 1:2] / 255).round().astype(np.uint16) & 0b111111) << 5
    b =  (32 * img[..., 2:3] / 255).round().astype(np.uint16) & 0b11111
    return r + g + b


def rgb16_565_to_rgb32_888(img):
    """
    Convert the 16-bit RGB565 image to 32-bit RGB888.

    Args:
        img: the 32-bit image in HWC format and RGB565 color space

    Returns:
        the 32-bit image in HWC format in RGB888 color space

    """
    r = (255.0 * ((img >> 11) & 0b11111)  / 32.0).round().astype(np.uint8)
    g = (255.0 * ((img >> 5)  & 0b111111) / 64.0).round().astype(np.uint8)
    b = (255.0 * ((img)       & 0b11111)  / 32.0).round().astype(np.uint8)
    return np.concatenate([r, g, b], axis=-1)


# explicitly define the outward facing API of this module
__all__ = [
    'NES_PALETTE',
    rgb2nes.__name__,
    nes2rgb.__name__,
    rgb32_888_to_rgb16_565.__name__,
    rgb16_565_to_rgb32_888.__name__,
]
