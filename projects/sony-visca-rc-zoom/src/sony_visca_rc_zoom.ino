#include <SoftwareSerial.h>

const byte rcPin = 3;
const byte cameraRxPin = 10;  // Not connected: transmit-only example.
const byte cameraTxPin = 11;  // Connect to camera RxD.

SoftwareSerial cameraSerial(cameraRxPin, cameraTxPin);

const byte addressSet[]     = {0x88, 0x30, 0x01, 0xFF};
const byte interfaceClear[] = {0x88, 0x01, 0x00, 0x01, 0xFF};
const byte zoomIn[]         = {0x81, 0x01, 0x04, 0x07, 0x23, 0xFF};
const byte zoomOut[]        = {0x81, 0x01, 0x04, 0x07, 0x33, 0xFF};
const byte zoomStop[]       = {0x81, 0x01, 0x04, 0x07, 0x00, 0xFF};

enum ZoomState { STOPPED, TELE, WIDE };
ZoomState lastState = STOPPED;

template <size_t N>
void sendPacket(const byte (&packet)[N]) {
  cameraSerial.write(packet, N);
}

void setup() {
  pinMode(rcPin, INPUT);
  cameraSerial.begin(9600);

  delay(500);
  sendPacket(addressSet);
  delay(100);
  sendPacket(interfaceClear);
  delay(100);
  sendPacket(zoomStop);
}

void loop() {
  unsigned long pulse = pulseIn(rcPin, HIGH, 25000UL);
  ZoomState nextState = STOPPED;

  if (pulse != 0) {
    if (pulse > 1550) {
      nextState = TELE;
    } else if (pulse < 1400) {
      nextState = WIDE;
    }
  }

  if (nextState != lastState) {
    if (nextState == TELE) {
      sendPacket(zoomIn);
    } else if (nextState == WIDE) {
      sendPacket(zoomOut);
    } else {
      sendPacket(zoomStop);
    }
    lastState = nextState;
  }
}
