
#include <cstring>
#include <cstdint>
#include <cstdlib>
#include <cstdio>
#include "nes_ntsc.h"

// Windows-base systems
#if defined(_WIN32) || defined(WIN32) || defined(__CYGWIN__) || defined(__MINGW32__) || defined(__BORLANDC__)
    // setup the module initializer. required to link visual studio C++ ctypes
    void PyInit_lib_nes_env() { }
    // setup the function modifier to export in the DLL
    #define EXP __declspec(dllexport)
// Unix-like systems
#else
    // setup the modifier as a dummy
    #define EXP
#endif

// definitions of functions for the Python interface to access
extern "C" {

// -----------------------------------------------------------------------
// MARK: Constants
// -----------------------------------------------------------------------

/// @brief Return the height in pixels, i.e., number of vertical scan lines.
///
/// @returns the height of the image in pixels
///
EXP uint32_t NES_NTSC_HEIGHT() { return 240; }

/// @brief Return the width in pixels, i.e., number of dots per scan line.
///
/// @returns the width of the input image in pixels
///
EXP uint32_t NES_NTSC_WIDTH_INPUT() { return 256; }

/// @brief Return the width in pixels, i.e., number of dots per scan line.
///
/// @returns the width of the output image in pixels
///
EXP uint32_t NES_NTSC_WIDTH_OUTPUT() {
    return NES_NTSC_OUT_WIDTH(NES_NTSC_WIDTH_INPUT());
}

/// @brief Return the number of bytes in a row of pixels.
///
/// @returns the number of bytes in each row of output pixels
///
EXP uint32_t NES_NTSC_PITCH() {
    return NES_NTSC_WIDTH_OUTPUT() * sizeof(uint32_t);
}

// -----------------------------------------------------------------------
// MARK: Configuration
// -----------------------------------------------------------------------

/// @brief Initialize a new `nes_ntsc_t` and return a pointer to it.
///
/// @returns a pointer to the newly creating `nes_ntsc_t` instance
///
EXP nes_ntsc_t* NES_NTSC_InitializeConfiguration() {
    return new nes_ntsc_t;
}

/// @brief Destroy an existing instance of `nes_ntsc_t`.
///
/// @param ntsc a pointer to an `nes_ntsc_t` to free from memory
///
EXP void NES_NTSC_DestroyConfiguration(nes_ntsc_t* ntsc) { free(ntsc); }

// -----------------------------------------------------------------------
// MARK: Setup
// -----------------------------------------------------------------------

/// @brief Initialize a new `nes_ntsc_t` and return a pointer to it.
///
/// @returns a pointer to the newly creating `nes_ntsc_t` instance
///
EXP nes_ntsc_setup_t* NES_NTSC_InitializeSetup() {
    return new nes_ntsc_setup_t{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
}

/// @brief Destroy an existing instance of `nes_ntsc_t`.
///
/// @param ntsc a pointer to `nes_ntsc_t` to free from memory
///
EXP void NES_NTSC_DestroySetup(nes_ntsc_setup_t* setup) { free(setup); }

/// @brief Set the setup object to the Composite preset.
///
/// @param setup the setup instance to setup to the Composite preset
///
EXP void NES_NTSC_SetupComposite(nes_ntsc_setup_t* setup) {
    memcpy(setup, &nes_ntsc_composite, sizeof(nes_ntsc_setup_t));
}

/// @brief Set the setup object to the S-Video preset.
///
/// @param setup the setup instance to setup to the S-Video preset
///
EXP void NES_NTSC_SetupSVideo(nes_ntsc_setup_t* setup) {
    memcpy(setup, &nes_ntsc_svideo, sizeof(nes_ntsc_setup_t));
}

/// @brief Set the setup object to the RGB preset.
///
/// @param setup the setup instance to setup to the RGB preset
///
EXP void NES_NTSC_SetupRGB(nes_ntsc_setup_t* setup) {
    memcpy(setup, &nes_ntsc_rgb, sizeof(nes_ntsc_setup_t));
}

/// @brief Set the setup object to the Monochrome preset.
///
/// @param setup the setup instance to setup to the Monochrome preset
///
EXP void NES_NTSC_SetupMonochrome(nes_ntsc_setup_t* setup) {
    memcpy(setup, &nes_ntsc_monochrome, sizeof(nes_ntsc_setup_t));
}

/// @brief Apply the setup to the given instance of `nes_ntsc_t`.
///
/// @param ntsc the instance of the filter to apply the setup to
/// @param setup the setup parameters to use when filtering images
///
EXP void NES_NTSC_SetupApply(nes_ntsc_t* ntsc, nes_ntsc_setup_t* setup) {
    nes_ntsc_init(ntsc, setup);
}

// -----------------------------------------------------------------------
// MARK: Pixel Buffers
// -----------------------------------------------------------------------

/// @brief Initialize a tensor for the input pixels in NES palette format.
///
/// @returns a pointer to the internal screen data structure as a vector
/// representation of a matrix of height matching the visible scans lines and
/// width matching the number of visible scan line dots. the data type is
/// 8-bit NES pixel index corresponding to a value in the NES palettes
///
EXP uint8_t* NES_NTSC_InitializeInputPixels() {
    // calculate the total number of bytes in the pixel buffer
    static const uint32_t BYTES = NES_NTSC_HEIGHT() * NES_NTSC_WIDTH_INPUT();
    return reinterpret_cast<uint8_t*>(calloc(BYTES, sizeof(uint8_t)));
}

/// @brief Free an input pixel buffer from memory.
///
/// @param pixels the buffer of pixels to free from memory
///
EXP void NES_NTSC_DestroyInputPixels(uint8_t* pixels) { free(pixels); }

/// @brief Initialize a tensor for the output pixels in RGBx format.
///
/// @returns a pointer to the matrix of 32-bit pixels
///
EXP uint32_t* NES_NTSC_InitializeOutputPixels() {
    // calculate the total number of bytes in the pixel buffer
    static const uint32_t BYTES = NES_NTSC_HEIGHT() * NES_NTSC_WIDTH_OUTPUT();
    return reinterpret_cast<uint32_t*>(calloc(BYTES, sizeof(uint32_t)));
}

/// @brief Free an output pixel buffer from memory.
///
/// @param pixels the buffer of pixels to free from memory
///
EXP void NES_NTSC_DestroyOutputPixels(uint32_t* pixels) { free(pixels); }

// -----------------------------------------------------------------------
// MARK: Processing
// -----------------------------------------------------------------------

/// @brief Process a step with the image filter.
///
/// @param output_pixels the output pixel buffer to store into created by
/// `NES_NTSC_InitializeOutputPixels`
/// @param input_pixels the input pixel buffer to read NES pixels from created
/// by `NES_NTSC_InitializeInputPixels`
/// @param ntsc the ntsc instance created by `NES_NTSC_InitializeConfiguration`
/// @param is_even_frame whether this frame is even to emulate the flickering
/// effect on every other frame
///
EXP void NES_NTSC_Process(
    uint32_t* const output_pixels,
    const uint8_t* const input_pixels,
    const nes_ntsc_t* const ntsc,
    bool is_even_frame = false
) {
    nes_ntsc_blit(
        ntsc,                    // configured NTSC object
        input_pixels,            // input buffer of NES pixels
        NES_NTSC_WIDTH_INPUT(),  // width of the NES screen
        is_even_frame,           // alternating frame flag
        NES_NTSC_WIDTH_INPUT(),  // width of the NES screen
        NES_NTSC_HEIGHT(),       // height of the NES screen
        output_pixels,           // output buffer to write to
        NES_NTSC_PITCH()         // number of bytes in an output row
    );
}

}  // extern "C"

// un-define the macro
#undef EXP
