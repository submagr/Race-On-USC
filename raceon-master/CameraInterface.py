#!/usr/bin/env python
# coding: utf-8

# In[89]:


from picamera.array import PiYUVArray, PiRGBArray
from picamera import PiCamera
from scipy.signal import find_peaks, butter, filtfilt
import time
import matplotlib.pyplot as plt
import skimage as ski

res = (640, 480)

camera = PiCamera()
camera.sensor_mode = 7
camera.resolution = res
camera.framerate = 120

# Initialize the buffer and start capturing
rawCapture = PiRGBArray(camera, size=res)
stream = camera.capture_continuous(rawCapture, format="rgb", use_video_port=True)

rawCapture.truncate(0)
frame = next(stream)

I = ski.color.rgb2gray(frame.array[0:320, 0:240, :])
plt.imshow(frame.array)
stream.close()
rawCapture.close()
camera.close()

