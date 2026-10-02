# Cascading IVPort Raspberry Pi Camera Multiplexers

<img src="images/setup.jpg" alt="Six-camera Raspberry Pi setup using cascaded IVPort CSI camera multiplexer boards" width="760">

This 2017 build cascaded several **IVPort Raspberry Pi camera multiplexer** boards so one Raspberry Pi CSI interface could select among six camera positions.

Read the original build article: **[Multiple Raspberry Pi cameras using cascaded IVPort multiplexers](https://www.eladorbach.com/2017/06/multiple-raspberry-pi-cameras-using.html)**.

## Important limitation

This is **sequential switching**, not simultaneous multi-camera capture. Only one camera path should drive the CSI connection at a time.

The original 2017 GPIO selector is preserved under [`legacy/`](legacy/) with its published pin assignments and route states.

## Original Raspberry Pi GPIO pin groups

The blog used physical Raspberry Pi **BOARD** numbering:

| Board | Enable | Select A | Select B |
|---|---:|---:|---:|
| 1 | 7 | 26 | 33 |
| 2 | 37 | 38 | 40 |
| 3 | 35 | 32 | 36 |

`src/ivport_selector.py` reconstructs the six routes from the published GPIO states while keeping camera capture out of the selector itself.

## Why camera capture is separate

The original experiment used the legacy `picamera` Python library. Current Raspberry Pi OS uses the libcamera-based camera stack and Picamera2. Keeping mux selection separate makes it possible to test the GPIO routing independently and then integrate the selector with the camera API appropriate to the Pi/IVPort revision.

## Usage

```python
from ivport_selector import IVPortSelector

selector = IVPortSelector()
try:
    selector.select(1)
    # Open/configure/capture using your camera stack here.
finally:
    selector.cleanup()
```

## Before connecting hardware

IVPort board revisions differ. Confirm the solder bridges, enable polarity, select truth table and camera numbering for the exact boards in hand before relying on these routes. Test one route at a time and allow the selected camera path to settle before capture.
