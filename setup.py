"""The setup script for installing and distributing the ntsc-py package."""
from glob import glob
import os
from setuptools import setup, find_packages, Extension


# set the compiler for the C++ framework
os.environ['CC'] = 'g++'
os.environ['CCX'] = 'g++'


# read the contents from the README file
with open('README.md') as README_file:
    README = README_file.read()


# The prefix name for the .so library to build. It will follow the format
# ntsc.*.so where the * changes depending on the build system
LIB_NAME = 'ntsc_py.lib_ntsc'
# The source files for building the extension. Globs locate all the cpp files
# used by the NTSC C++ subproject. MANIFEST.in has to include the blanket
# "cpp" directory to ensure that the .inc file gets included too
SOURCES = glob('ntsc_py/ntsc/src/*.cpp')
# The directory pointing to header files used by the NTSC cpp files.
# This directory has to be included using MANIFEST.in too to include the
# headers with sdist
INCLUDE_DIRS = ['ntsc_py/ntsc/include']
# Build arguments to pass to the compiler
EXTRA_COMPILE_ARGS = ['-std=c++1y', '-march=native', '-pipe', '-O3']
# The official extension using the name, source, headers, and build args
LIB_NTSC = Extension(LIB_NAME,
    sources=SOURCES,
    include_dirs=INCLUDE_DIRS,
    extra_compile_args=EXTRA_COMPILE_ARGS,
)


setup(
    name='ntsc_py',
    version='0.2.0',
    description='An interface to various graphical NTSC filters.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='NTSC Graphics Filter',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        # 'Intended Audience :: Developers',
        # 'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        # 'Topic :: Games/Entertainment',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: System :: Emulators',
    ],
    url='https://github.com/Kautenja/ntsc-py',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    ext_modules=[LIB_NTSC],
    zip_safe=False,
    # install_requires=[
    #     'gym>=0.17.2',
    #     'numpy>=1.18.5',
    #     'pyglet<=1.5.0,>=1.4.0',
    #     'tqdm>=4.48.2',
    # ],
    # entry_points={
    #     'console_scripts': [
    #         'ntsc_py = ntsc_py.app.cli:main',
    #     ],
    # },
)
