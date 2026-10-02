// Historical ATtiny85 sketch from the 2014 blog post.
// Blogger whitespace normalized.

#include <SoftwareSerial.h>

#define zoom PB0
#define rxPin PB1
#define txPin PB2

SoftwareSerial mySerial(rxPin, txPin);

byte address_set[4] = {0x88, 0x30, 0x01, 0xFF};
byte if_clear[5] = {0x88, 0x01, 0x00, 0x01, 0xFF};
byte command_cancel[3] = {0x81, 0x21, 0xFF};
byte zoom_teleVar[6] = {0x81, 0x01, 0x04, 0x07, 0x23, 0xFF};
byte zoom_wideVar[6] = {0x81, 0x01, 0x04, 0x07, 0x33, 0xFF};
byte zoom_stop[6] = {0x81, 0x01, 0x04, 0x07, 0x00, 0xFF};
byte auto_focus[6] = {0x81, 0x01, 0x04, 0x38, 0x02, 0xFF};
const int thisdelay = 250;

void setup() {
  pinMode(rxPin, INPUT);
  pinMode(txPin, OUTPUT);
  pinMode(zoom, INPUT);
  mySerial.begin(9600);
  for (int i = 0; i < 4; i++) mySerial.write(address_set[i]);
  delay(thisdelay);
  for (int i = 0; i < 5; i++) {
    mySerial.write(if_clear[i]);
    delay(thisdelay);
  }
}

void loop() {
  int zoom_inState = pulseIn(zoom, HIGH, 25000);
  if (zoom_inState > 1550) {
    delay(thisdelay);
    for (int i = 0; i < 6; i++) mySerial.write(zoom_teleVar[i]);
  }

  int zoom_outState = pulseIn(zoom, HIGH, 25000);
  if (zoom_outState < 1400) {
    delay(thisdelay);
    for (int i = 0; i < 6; i++) mySerial.write(zoom_wideVar[i]);
  }

  if (zoom_outState < 1500 && zoom_inState > 1400) {
    for (int i = 0; i < 6; i++) mySerial.write(auto_focus[i]);
    for (int i = 0; i < 6; i++) mySerial.write(zoom_stop[i]);
  }
}

void sendcommand_cancel() {
  for (int i = 0; i < 3; i++) mySerial.write(command_cancel[i]);
}
