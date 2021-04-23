// The library definition of the SMS NTSC library.
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
#include "sms_ntsc.h"
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
EXP uint32_t SMS_NTSC_HEIGHT() { return 240; }

/// @brief Return the width in pixels, i.e., number of dots per scan line.
///
/// @returns the width of the input image in pixels
///
EXP uint32_t SMS_NTSC_WIDTH_INPUT() { return 256; }

/// @brief Return the width in pixels, i.e., number of dots per scan line.
///
/// @returns the width of the output image in pixels
///
EXP uint32_t SMS_NTSC_WIDTH_OUTPUT() {
    return SMS_NTSC_OUT_WIDTH(SMS_NTSC_WIDTH_INPUT());
}

/// @brief Return the number of bytes in a row of pixels.
///
/// @returns the number of bytes in each row of output pixels
///
EXP uint32_t SMS_NTSC_PITCH() {
    return SMS_NTSC_WIDTH_OUTPUT() * sizeof(uint32_t);
}

// -----------------------------------------------------------------------
// MARK: Configuration
// -----------------------------------------------------------------------

/// @brief Initialize a new `sms_ntsc_t` and return a pointer to it.
///
/// @returns a pointer to the newly creating `sms_ntsc_t` instance
///
EXP sms_ntsc_t* SMS_NTSC_InitializeConfiguration() {
    return new sms_ntsc_t;
}

/// @brief Destroy an existing instance of `sms_ntsc_t`.
///
/// @param ntsc a pointer to an `sms_ntsc_t` to free from memory
///
EXP void SMS_NTSC_DestroyConfiguration(sms_ntsc_t* ntsc) { free(ntsc); }

// -----------------------------------------------------------------------
// MARK: Setup
// -----------------------------------------------------------------------

/// @brief Initialize a new `sms_ntsc_t` and return a pointer to it.
///
/// @returns a pointer to the newly creating `sms_ntsc_t` instance
///
EXP sms_ntsc_setup_t* SMS_NTSC_InitializeSetup() {
    return new sms_ntsc_setup_t{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
}

/// @brief Destroy an existing instance of `sms_ntsc_t`.
///
/// @param ntsc a pointer to `sms_ntsc_t` to free from memory
///
EXP void SMS_NTSC_DestroySetup(sms_ntsc_setup_t* setup) { free(setup); }

/// @brief Set the setup object to the Composite preset.
///
/// @param setup the setup instance to setup to the Composite preset
///
EXP void SMS_NTSC_SetupComposite(sms_ntsc_setup_t* setup) {
    memcpy(setup, &sms_ntsc_composite, sizeof(sms_ntsc_setup_t));
}

/// @brief Set the setup object to the S-Video preset.
///
/// @param setup the setup instance to setup to the S-Video preset
///
EXP void SMS_NTSC_SetupSVideo(sms_ntsc_setup_t* setup) {
    memcpy(setup, &sms_ntsc_svideo, sizeof(sms_ntsc_setup_t));
}

/// @brief Set the setup object to the RGB preset.
///
/// @param setup the setup instance to setup to the RGB preset
///
EXP void SMS_NTSC_SetupRGB(sms_ntsc_setup_t* setup) {
    memcpy(setup, &sms_ntsc_rgb, sizeof(sms_ntsc_setup_t));
}

/// @brief Set the setup object to the Monochrome preset.
///
/// @param setup the setup instance to setup to the Monochrome preset
///
EXP void SMS_NTSC_SetupMonochrome(sms_ntsc_setup_t* setup) {
    memcpy(setup, &sms_ntsc_monochrome, sizeof(sms_ntsc_setup_t));
}

/// @brief Apply the setup to the given instance of `sms_ntsc_t`.
///
/// @param ntsc the instance of the filter to apply the setup to
/// @param setup the setup parameters to use when filtering images
///
EXP void SMS_NTSC_SetupApply(sms_ntsc_t* ntsc, sms_ntsc_setup_t* setup) {
    sms_ntsc_init(ntsc, setup);
}

// -----------------------------------------------------------------------
// MARK: Pixel Buffers
// -----------------------------------------------------------------------

/// @brief Initialize a tensor for the input pixels in SMS palette format.
///
/// @returns a pointer to the internal screen data structure as a vector
/// representation of a matrix of height matching the visible scans lines and
/// width matching the number of visible scan line dots. the data type is
/// 16-bit SMS pixel index corresponding to a value in the SMS palettes
///
EXP uint16_t* SMS_NTSC_InitializeInputPixels() {
    // calculate the total number of bytes in the pixel buffer
    static const uint32_t BYTES = SMS_NTSC_HEIGHT() * SMS_NTSC_WIDTH_INPUT();
    return reinterpret_cast<uint16_t*>(calloc(BYTES, sizeof(uint16_t)));
}

/// @brief Free an input pixel buffer from memory.
///
/// @param pixels the buffer of pixels to free from memory
///
EXP void SMS_NTSC_DestroyInputPixels(uint16_t* pixels) { free(pixels); }

/// @brief Initialize a tensor for the output pixels in RGBx format.
///
/// @returns a pointer to the matrix of 32-bit pixels
///
EXP uint32_t* SMS_NTSC_InitializeOutputPixels() {
    // calculate the total number of bytes in the pixel buffer
    static const uint32_t BYTES = SMS_NTSC_HEIGHT() * SMS_NTSC_WIDTH_OUTPUT();
    return reinterpret_cast<uint32_t*>(calloc(BYTES, sizeof(uint32_t)));
}

/// @brief Free an output pixel buffer from memory.
///
/// @param pixels the buffer of pixels to free from memory
///
EXP void SMS_NTSC_DestroyOutputPixels(uint32_t* pixels) { free(pixels); }

// -----------------------------------------------------------------------
// MARK: Processing
// -----------------------------------------------------------------------

/// @brief Process a step with the image filter.
///
/// @param output_pixels the output pixel buffer to store into created by
/// `SMS_NTSC_InitializeOutputPixels`
/// @param input_pixels the input pixel buffer to read SMS pixels from created
/// by `SMS_NTSC_InitializeInputPixels`
/// @param ntsc the ntsc instance created by `SMS_NTSC_InitializeConfiguration`
///
EXP void SMS_NTSC_Process(
    uint32_t* const output_pixels,
    const uint16_t* const input_pixels,
    const sms_ntsc_t* const ntsc
) {
    sms_ntsc_blit(
        ntsc,                     // configured NTSC object
        input_pixels,             // input buffer of SMS pixels
        SMS_NTSC_WIDTH_INPUT(),   // width of the SMS screen
        SMS_NTSC_WIDTH_INPUT(),   // width of the SMS screen
        SMS_NTSC_HEIGHT(),        // height of the SMS screen
        output_pixels,            // output buffer to write to
        SMS_NTSC_PITCH()          // number of bytes in an output row
    );
}

}  // extern "C"
