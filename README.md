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
filter = NES_NTSC()
```

The `setup` function can be used to configure the parameters of the filter. The
same parameters of the `setup` function can be passed to the constructor on
initialization of the filter. See the table below for a description of each of
the parameters for the setup function

```python
filter.setup(mode='composite', gamma=1, artifacts=2, sharpness=0.4, ...)
```

| Parameter      | Values | Description |
|:---------------|:-------|:------------|
| `mode`         |        |             |
| `hue`          |        |             |
| `saturation`   |        |             |
| `contrast`     |        |             |
| `brightness`   |        |             |
| `sharpness`    |        |             |
| `gamma`        |        |             |
| `resolution`   |        |             |
| `artifacts`    |        |             |
| `fringing`     |        |             |
| `bleed`        |        |             |
| `merge_fields` |        |             |
