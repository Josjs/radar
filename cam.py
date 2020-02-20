import cv2
import picamera
import picamera.array
import numpy as np
import time

#Capture single frame
def capture_frame(mode=0):
    modes = [(640,480), (2592,1952)]
    print("mode =", modes[mode])
    cam = picamera.PiCamera(
        resolution = modes[mode],
        # framerate_range = 10
        )
    cam.awb_mode = "cloudy"
    rawCapture = picamera.array.PiRGBArray(cam, size=modes[mode])
    time.sleep(0.1)
    cam.capture(rawCapture, format="bgr")
    img = rawCapture
    rawCapture.truncate(0)
    return img.array
#
def save_frame(path, frame):
    cv2.imwrite(path, frame)

