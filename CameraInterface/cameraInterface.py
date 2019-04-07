from picamera.array import PiYUVArray, PiRGBArray
from picamera import PiCamera
from scipy.signal import find_peaks, butter, filtfilt
import time
import matplotlib.pyplot as plt
import skimage as ski
import io
from PIL import Image

def cameraInterface:
    def __init__(self, res = (640, 480)):
        self.res = res
        camera = PiCamera()
        camera.sensor_mode = 7
        camera.resolution = res
        time.sleep(2)
        camera.framerate = 90
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        self.camera = camera

    def getImage(self):
        # Initialize the buffer and start capturing
        rawCapture = PiRGBArray(self.camera, size=self.res)
        stream = self.camera.capture_continuous(rawCapture, format="rgb", use_video_port=True)
        I = ski.color.rgb2gray(frame.array[0:320, 0:240, :])
        stream.close()
        rawCapture.close()
        camera.close()
        
        plt.imshow(frame.array)
        
        
        b, a = butter(3, 0.02)
        # Create the in-memory stream
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)
            camera.capture(stream, format='jpeg')
        # "Rewind" the stream to the beginning so we can read its content
        stream.seek(0)
        image = Image.open(stream)