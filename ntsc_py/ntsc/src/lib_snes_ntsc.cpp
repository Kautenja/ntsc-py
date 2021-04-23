// The library definition of the SNES NTSC library.
// Copyright 2021 Christian Kauten
//
// Author: Christian Kauten (kautenja@auburn.edu)
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#include <cstring>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include "snes_ntsc.h"
#include "lib_ntsc.h"

// definitions of functions for the Python interface to access
extern "C" {

// -----------------------------------------------------------------------
// MARK: Constants
// -----------------------------------------------------------------------

/// @brief Return the height in pixels, i.e., number of vertical scan lines.
///
/// @returns the height of the image in pixels
///
EXP uint32_t SNES_NTSC_HEIGHT() { return 240; }

/// @brief Return the width in pixels, i.e., number of dots per scan line.
///
/// @returns the width of the input image in pixels
///
EXP uint32_t SNES_NTSC_WIDTH_INPUT() { return 256; }

/// @brief Return the width in pixels, i.e., number of dots per scan line.
///
/// @returns the width of the output image in pixels
///
EXP uint32_t SNES_NTSC_WIDTH_OUTPUT() {
    return SNES_NTSC_OUT_WIDTH(SNES_NTSC_WIDTH_INPUT());
}

/// @brief Return the number of bytes in a row of pixels.
///
/// @returns the number of bytes in each row of output pixels
///
EXP uint32_t SNES_NTSC_PITCH() {
    return SNES_NTSC_WIDTH_OUTPUT() * sizeof(uint32_t);
}

// -----------------------------------------------------------------------
// MARK: Configuration
// -----------------------------------------------------------------------

/// @brief Initialize a new `snes_ntsc_t` and return a pointer to it.
///
/// @returns a pointer to the newly creating `snes_ntsc_t` instance
///
EXP snes_ntsc_t* SNES_NTSC_InitializeConfiguration() {
    return new snes_ntsc_t;
}

/// @brief Destroy an existing instance of `snes_ntsc_t`.
///
/// @param ntsc a pointer to an `snes_ntsc_t` to free from memory
///
EXP void SNES_NTSC_DestroyConfiguration(snes_ntsc_t* ntsc) { free(ntsc); }

// -----------------------------------------------------------------------
// MARK: Setup
// -----------------------------------------------------------------------

/// @brief Initialize a new `snes_ntsc_t` and return a pointer to it.
///
/// @returns a pointer to the newly creating `snes_ntsc_t` instance
///
EXP snes_ntsc_setup_t* SNES_NTSC_InitializeSetup() {
    return new snes_ntsc_setup_t{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
}

/// @brief Destroy an existing instance of `snes_ntsc_t`.
///
/// @param ntsc a pointer to `snes_ntsc_t` to free from memory
///
EXP void SNES_NTSC_DestroySetup(snes_ntsc_setup_t* setup) { free(setup); }

/// @brief Set the setup object to the Composite preset.
///
/// @param setup the setup instance to setup to the Composite preset
///
EXP void SNES_NTSC_SetupComposite(snes_ntsc_setup_t* setup) {
    memcpy(setup, &snes_ntsc_composite, sizeof(snes_ntsc_setup_t));
}

/// @brief Set the setup object to the S-Video preset.
///
/// @param setup the setup instance to setup to the S-Video preset
///
EXP void SNES_NTSC_SetupSVideo(snes_ntsc_setup_t* setup) {
    memcpy(setup, &snes_ntsc_svideo, sizeof(snes_ntsc_setup_t));
}

/// @brief Set the setup object to the RGB preset.
///
/// @param setup the setup instance to setup to the RGB preset
///
EXP void SNES_NTSC_SetupRGB(snes_ntsc_setup_t* setup) {
    memcpy(setup, &snes_ntsc_rgb, sizeof(snes_ntsc_setup_t));
}

/// @brief Set the setup object to the Monochrome preset.
///
/// @param setup the setup instance to setup to the Monochrome preset
///
EXP void SNES_NTSC_SetupMonochrome(snes_ntsc_setup_t* setup) {
    memcpy(setup, &snes_ntsc_monochrome, sizeof(snes_ntsc_setup_t));
}

/// @brief Apply the setup to the given instance of `snes_ntsc_t`.
///
/// @param ntsc the instance of the filter to apply the setup to
/// @param setup the setup parameters to use when filtering images
///
EXP void SNES_NTSC_SetupApply(snes_ntsc_t* ntsc, snes_ntsc_setup_t* setup) {
    snes_ntsc_init(ntsc, setup);
}

// -----------------------------------------------------------------------
// MARK: Pixel Buffers
// -----------------------------------------------------------------------

/// @brief Initialize a tensor for the input pixels in SNES palette format.
///
/// @returns a pointer to the internal screen data structure as a vector
/// representation of a matrix of height matching the visible scans lines and
/// width matching the number of visible scan line dots. the data type is
/// 16-bit SNES pixel index corresponding to a value in the SNES palettes
///
EXP uint16_t* SNES_NTSC_InitializeInputPixels() {
    // calculate the total number of bytes in the pixel buffer
    static const uint32_t BYTES = SNES_NTSC_HEIGHT() * SNES_NTSC_WIDTH_INPUT();
    return reinterpret_cast<uint16_t*>(calloc(BYTES, sizeof(uint16_t)));
}

/// @brief Free an input pixel buffer from memory.
///
/// @param pixels the buffer of pixels to free from memory
///
EXP void SNES_NTSC_DestroyInputPixels(uint16_t* pixels) { free(pixels); }

/// @brief Initialize a tensor for the output pixels in RGBx format.
///
/// @returns a pointer to the matrix of 32-bit pixels
///
EXP uint32_t* SNES_NTSC_InitializeOutputPixels() {
    // calculate the total number of bytes in the pixel buffer
    static const uint32_t BYTES = SNES_NTSC_HEIGHT() * SNES_NTSC_WIDTH_OUTPUT();
    return reinterpret_cast<uint32_t*>(calloc(BYTES, sizeof(uint32_t)));
}

/// @brief Free an output pixel buffer from memory.
///
/// @param pixels the buffer of pixels to free from memory
///
EXP void SNES_NTSC_DestroyOutputPixels(uint32_t* pixels) { free(pixels); }

// -----------------------------------------------------------------------
// MARK: Processing
// -----------------------------------------------------------------------

/// @brief Process a step with the image filter.
///
/// @param output_pixels the output pixel buffer to store into created by
/// `SNES_NTSC_InitializeOutputPixels`
/// @param input_pixels the input pixel buffer to read SNES pixels from created
/// by `SNES_NTSC_InitializeInputPixels`
/// @param ntsc the ntsc instance created by `SNES_NTSC_InitializeConfiguration`
/// @param is_even_frame whether this frame is even to emulate the flickering
/// effect on every other frame
///
EXP void SNES_NTSC_Process(
    uint32_t* const output_pixels,
    const uint16_t* const input_pixels,
    const snes_ntsc_t* const ntsc,
    bool is_even_frame = false
) {
    snes_ntsc_blit(
        ntsc,                     // configured NTSC object
        input_pixels,             // input buffer of SNES pixels
        SNES_NTSC_WIDTH_INPUT(),  // width of the SNES screen
        is_even_frame,            // alternating frame flag
        SNES_NTSC_WIDTH_INPUT(),  // width of the SNES screen
        SNES_NTSC_HEIGHT(),       // height of the SNES screen
        output_pixels,            // output buffer to write to
        SNES_NTSC_PITCH()         // number of bytes in an output row
    );
}

}  // extern "C"
