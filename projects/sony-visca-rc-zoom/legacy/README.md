# Historical source

The 2014 post included two sketches: a regular Arduino version using the hardware `Serial` port and an ATtiny85 version using `SoftwareSerial`. The files here preserve those command values and thresholds with whitespace normalized from Blogger.

The cleaned version in `../src/` is transmit-only and intentionally avoids feeding the camera's 5 V CMOS TX signal into a 3.3 V MCU input.
