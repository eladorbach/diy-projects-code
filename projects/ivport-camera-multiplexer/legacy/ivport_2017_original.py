# Historical code from the 2017 blog post.
# Whitespace normalized from Blogger; GPIO states preserved.

import time
import picamera
import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BOARD)

e21, p21, p22 = 7, 26, 33
e31, p31, p32 = 37, 38, 40
e41, p41, p42 = 35, 32, 36

for pin in (e21, p21, p22, e31, p31, p32, e41, p41, p42):
    gp.setup(pin, gp.OUT)

# Initialize boards.
gp.output(e21, False); gp.output(p21, False); gp.output(p22, True)
gp.output(e31, False); gp.output(p31, False); gp.output(p32, True)
gp.output(e41, False); gp.output(p41, False); gp.output(p42, True)

frames = 1
focus = 0
cam = 1

def cam_change():
    global cam
    gp.setmode(gp.BOARD)

    if cam == 1:
        gp.output(e21, True); gp.output(p21, True); gp.output(p22, False)
        gp.output(e31, False); gp.output(p31, False); gp.output(p32, True)
        print("now camera 1")
    elif cam == 2:
        gp.output(e21, True); gp.output(p21, True); gp.output(p22, False)
        gp.output(e31, True); gp.output(p31, False); gp.output(p32, True)
        print("now camera 2")
    elif cam == 3:
        gp.output(e21, True); gp.output(p21, True); gp.output(p22, False)
        gp.output(e31, False); gp.output(p31, True); gp.output(p32, False)
        print("now camera 3")
    elif cam == 4:
        gp.output(e21, True); gp.output(p21, True); gp.output(p22, False)
        gp.output(e31, True); gp.output(p31, True); gp.output(p32, False)
        gp.output(e41, False); gp.output(p41, True); gp.output(p42, False)
        print("now camera 4")
    elif cam == 5:
        gp.output(e21, True); gp.output(p21, True); gp.output(p22, False)
        gp.output(e31, True); gp.output(p31, True); gp.output(p32, False)
        gp.output(e41, True); gp.output(p41, True); gp.output(p42, False)
        print("now camera 5")
    elif cam == 6:
        gp.output(e21, True); gp.output(p21, False); gp.output(p22, True)
        print("now camera 6")

    time.sleep(focus)
    cam += 1
    if cam > 6:
        print("reset count to camera 1")
        cam = 1
