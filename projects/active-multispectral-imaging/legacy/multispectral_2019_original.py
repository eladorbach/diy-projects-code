# Historical code from the 2019 blog post.
# Whitespace normalized from Blogger; behavior intentionally preserved.

from __future__ import division

import time
import Adafruit_PCA9685
import cv2
from pyueye import ueye
import ctypes
import datetime

pwm = Adafruit_PCA9685.PCA9685(address=0x40)  # 1st
pwm1 = Adafruit_PCA9685.PCA9685(address=0x41)  # 2nd
pwm2 = Adafruit_PCA9685.PCA9685(address=0x42)  # 3rd

pwm.set_pwm_freq(1000)
pwm1.set_pwm_freq(1000)
pwm2.set_pwm_freq(1000)

spec = "avo_leaf"  # name of specimen
led = list(range(32))
lux = list(range(1900, 1932))  # temporary initial value, 0..4095

for x, y in zip(led, lux):
    if x < 16:
        pwm.set_pwm(x, y, 0)
    elif 14 < x < 32:
        pwm1.set_pwm(x - 16, y, 0)
    elif 31 < x < 33:
        pwm2.set_pwm(x - 32, y, 0)
    else:
        print(x)

    hcam = ueye.HIDS(1)
    pccmem = ueye.c_mem_p()
    memID = ueye.c_int()
    hWnd = ctypes.c_voidp()
    ueye.is_InitCamera(hcam, hWnd)

    sensorinfo = ueye.SENSORINFO()
    ueye.is_GetSensorInfo(hcam, sensorinfo)
    ueye.is_AllocImageMem(
        hcam, sensorinfo.nMaxWidth, sensorinfo.nMaxHeight, 24, pccmem, memID
    )
    ueye.is_SetImageMem(hcam, pccmem, memID)
    nret = ueye.is_FreezeVideo(hcam, ueye.IS_WAIT)
    print("camera" if nret == 0 else "____problem!!!____")

    FileParams = ueye.IMAGE_FILE_PARAMS()
    FileParams.pwchFileName = (
        spec + "_led_" + str(x + 1) + "_cam_"
        + datetime.datetime.now().strftime("%s") + ".bmp"
    )
    FileParams.nFileType = ueye.IS_IMG_BMP
    FileParams.ppcImageMem = None
    FileParams.pnImageID = None
    nret = ueye.is_ImageFile(
        hcam, ueye.IS_IMAGE_FILE_CMD_SAVE, FileParams, ueye.sizeof(FileParams)
    )
    print("camera" if nret == 0 else "____problem!!!____")

    ueye.is_FreeImageMem(hcam, pccmem, memID)
    ueye.is_ExitCamera(hcam)

    if x < 16:
        pwm.set_pwm(x, 0, 0)
    elif 14 < x < 32:
        pwm1.set_pwm(x - 16, 0, 0)
    elif 31 < x < 33:
        pwm2.set_pwm(x - 32, 0, 0)
    else:
        print(x)
