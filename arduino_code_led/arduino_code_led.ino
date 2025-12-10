// ---------------------------------------------------------
// SAVE THIS FILE AS: AllPixelsOneCommand.ino
// ---------------------------------------------------------

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// PIN CONFIGURATION
#define PIN        6   // Pin connected to the NeoPixels
#define NUMPIXELS  8   // Number of NeoPixels in your strip/ring

// INITIALIZE NEOPIXEL OBJECT
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // Support for Trinket 5V 16MHz
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif

  pixels.begin();           // Initialize the NeoPixel strip
  pixels.setBrightness(50); // Optional: Set brightness (0-255) to save power/eyes
  pixels.show();            // Initialize all pixels to 'off'
}

void loop() {
  // ------------------------------------------------------
  // ONE COMMAND TO CHANGE ALL PIXELS
  // ------------------------------------------------------
  
  // Syntax: pixels.fill(color, first_pixel, count);
  
  // // Example 1: Set ALL pixels to Red
  // pixels.fill(pixels.Color(255, 0, 0), 0, NUMPIXELS);
  // pixels.show();
  // delay(1000);

  // Example 2: Set ALL pixels to Green
  pixels.fill(pixels.Color(255, 0, 255), 0, NUMPIXELS);

  pixels.show();
  delay(1000);

  // // Example 3: Set ALL pixels to Blue
  // pixels.fill(pixels.Color(0, 0, 255), 0, NUMPIXELS);
  // pixels.show();
  // delay(1000);
  
  // // Example 4: Turn ALL pixels OFF (Black)
  // pixels.fill(pixels.Color(0, 0, 0), 0, NUMPIXELS);
  // pixels.show();
  // delay(1000);
}