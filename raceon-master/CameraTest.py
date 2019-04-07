from picamera.array import PiYUVArray, PiRGBArray
from picamera import PiCamera
from scipy.signal import find_peaks, butter, filtfilt
import time
import matplotlib.pyplot as plt
import skimage as ski

res = (1024, 768)
camera = PiCamera()
camera.sensor_mode = 7
camera.resolution = res
camera.framerate = 120

# Initialize the buffer and start capturing
rawCapture = PiRGBArray(camera, size=res)
stream = camera.capture_continuous(rawCapture, format="rgb", use_video_port=True)
rawCapture.truncate(0)
frame = next(stream)

# Release resources
stream.close()
rawCapture.close()
camera.close()

b, a = butter(3, 0.02)

# Run a track detection algorithm on a single horizontal line.
# Uses YUV420 image format as the Y component corresponds to image intensity (gray image)
# and thus there is no need to convert from RGB to BW
camera = PiCamera()
camera.sensor_mode = 7
camera.resolution = res
camera.framerate = 120

print("Taking raw capture")
rawCapture = PiYUVArray(camera, size=res)
stream = camera.capture_continuous(rawCapture, format="yuv", use_video_port=True)

mid = 500
threshold = 250
for f in stream:
        # Get the intensity component of the image (a trick to get black and white images)
    I = f.array[:, :, 0]
    # Reset the buffer for the next image
    rawCapture.truncate(0)
    # Select a horizontal line in the middle of the image
    L = I[120, :]
    # Smooth the transitions so we can detect the peaks 
    Lf = filtfilt(b, a, L)

    # Find peaks which are higher than 0.5
    p = find_peaks(Lf, height=128)
    print("Peak Positions: ", p)
    if len(p[0]) > 0:
        peak_Position = p[0][int(len(p[0])/2)]
        disp = mid - peak_Position
    else:
        disp = 0
    print("displacement: ", disp)
    if disp < -1*threshold:
        print("go right")
    elif -1*threshold <= disp <= threshold:
        print("go straight")
    else:
        print("go left")