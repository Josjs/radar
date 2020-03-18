import cv2
import picamera
import picamera.array
import numpy as np
import time

# Capture single frame
def capture_frame(mode=0):
    modes = [(640,480), (2592,1952)]
    cam = picamera.PiCamera(
        resolution = modes[mode],
        # framerate_range = 10
        )
    cam.awb_mode = "tungsten"
    rawCapture = picamera.array.PiRGBArray(cam, size=modes[mode])
    time.sleep(0.1)
    cam.capture(rawCapture, format="bgr")
    cam.close()
    img = rawCapture
    rawCapture.truncate(0)
    return img.array

# Save frame as image
def save_frame(path, frame):
    cv2.imwrite(path, frame)

# Capture [duration] seconds of video, and save to path
def video(path, duration, mode=0):
    modes = [(640,480), (1920,1080)]
    with  picamera.PiCamera(resolution = modes[mode]) as cam:
        cam.awb_mode = "tungsten"
        # Camera setup time
        time.sleep(0.1)
        cam.start_recording(path, quality = 25)
        cam.wait_recording(duration)
        cam.stop_recording()
