# NTSC-py

[![build-status][]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://travis-ci.org/Kautenja/ntsc-py.svg
[ci-server]: https://travis-ci.org/Kautenja/ntsc-py
[pypi-version]: https://badge.fury.io/py/ntsc-py.svg
[pypi-license]: https://img.shields.io/pypi/l/ntsc-py.svg
[pypi-status]: https://img.shields.io/pypi/status/ntsc-py.svg
[pypi-format]: https://img.shields.io/pypi/format/ntsc-py.svg
[pypi-home]: https://badge.fury.io/py/ntsc-py
[python-version]: https://img.shields.io/pypi/pyversions/ntsc-py.svg
[python-home]: https://python.org

`ctypes` interfaces to Blargg's [NTSC filter libraries][Blargg-NTSC].

[Blargg-NTSC]: http://slack.net/~ant/libs/ntsc.html

<table align="center">
    <tr>
        <th>NES NTSC</th>
        <th>SNES NTSC</th>
        <th>SMS NTSC</th>
    </tr>
    <tr>
        <td>
            <img
                width="256"
                alt="NES NTSC"
                src="https://user-images.githubusercontent.com/2184469/115817023-a0fdca00-a3bf-11eb-9a87-faf1d527ddc6.gif"
            />
        </td>
        <td>
             <img
                width="256"
                alt="SNES NTSC"
                src="https://user-images.githubusercontent.com/2184469/115882317-45a8f780-a412-11eb-91bb-0ec593194e0e.gif"
            />
        </td>
        <td>
            <img
                width="256"
                alt="SMS NTSC"
                src="https://user-images.githubusercontent.com/2184469/115904006-e48d1e00-a429-11eb-967e-71c1ba2b01c5.gif"
            />
        </td>
    </tr>
</table>

# Installation

The preferred installation of `ntsc-py` is from `pip`:

```shell
pip install ntsc-py
```

## Debian

Make sure you have the `clang++` compiler installed:

```shell
sudo apt-get install clang
```

## Windows

You'll need to install the Visual-Studio 17.0 tools for Windows installation.
The [Visual Studio Community](https://visualstudio.microsoft.com/downloads/)
package provides these tools for free.

# Usage

<!-- ## Command Line Interface

To filter images from the command line, using the following command.

```shell
ntsc_py -i <input image path> -o <output image path>
```

To print out documentation for the command line interface execute:

```shell
ntsc_py -h
``` -->

## Python API

### NES NTSC

To use the NES NTSC filter, first create an instance:

```python
from ntsc_py import NES_NTSC
ntsc = NES_NTSC()
```

The `setup` function can be used to configure the parameters of the filter. The
same parameters of the `setup` function can be passed to the constructor on
initialization of the filter. See the table below for a description of each of
the parameters for the setup function

```python
ntsc.setup(mode='composite', gamma=1, artifacts=2, sharpness=0.4, ...)
```

| Parameter      | Stable Values                              | Description                                                     |
|:---------------|:-------------------------------------------|:----------------------------------------------------------------|
| `mode`         | `rgb`, `composite`, `svideo`, `monochrome` | Sets all parameters to a preset value.                          |
| `hue`          | _[-1.0, 1.0]_                              | Controls the hue of the image in degrees _[-180, 180]_.         |
| `saturation`   | _[-1.0, 1.0]_                              | Controls the saturation from monochrome to over-saturated.      |
| `contrast`     | _[-1.0, 1.0]_                              | Controls the contrast of the luminance in the image.            |
| `brightness`   | _[-1.0, 1.0]_                              | Controls the brightness from dark to bright.                    |
| `sharpness`    | _[-1.0, 1.0]_                              | Controls edge / contrast enhancement and blurring effects.      |
| `gamma`        | _[-1.0, 1.0]_                              | Adjusts the linearity of the luminance quantizer.               |
| `resolution`   | ?                                          | Controls the resolution of the image.                           |
| `artifacts`    | ?                                          | Controls influence of artifacts caused by color changes.        |
| `fringing`     | ?                                          | Controls influence of fringing caused by brightness changes.    |
| `bleed`        | ?                                          | Controls the amount of color bleed (color resolution reduction) |
| `merge_fields` | _[0, 1]_                                   | If true, merges even and off fields to reduce flicker.          |

Images can be filtered by assigning them to the input buffer of the image in
NES pixel format using the NES palette of 64 unique colors.

```python
ntsc.nes_pixels[:] = np.random.uniform(0, 63, ntsc.nes_pixels.shape)
```

Alternatively, RGB images can be converted to the NES palette using a mean
squared error fit.

```python
from ntsc_py import rgb2nes, nes2rgb
ntsc.nes_pixels[:] = rgb2nes(np.random.uniform(0, 255, ntsc.nes_pixels.shape[:2] + (3, )))
```

Once `nes_pixels` has been updated with new pixel data, call `process` to filter
the image and compute the RGB output in `ntsc_pixels`.

```python
ntsc.filter()
```

### SNES NTSC

Coming Soon!

### SMS NTSC

Coming Soon!
