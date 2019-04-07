
from picamera import PiCamera
from picamera.array import PiRGBArray, PiYUVArray
from scipy.signal import filtfilt, butter, find_peaks
from pwm import PWM
import sys
from time import sleep

if len(sys.argv) >=2 and sys.argv[1] == "P":
    debug = False
else:
    debug = True

b, a = butter(3, 0.007)

minSpeed =  1000000 # 0 speed
zeroRot  =  1000000
maxRot   =   500000
rot = zeroRot


pwm0 = PWM(0)  # motor
pwm0.export()
pwm0.period = 20000000
pwm0.duty_cycle = minSpeed

pwm1 = PWM(1)  # servo
pwm1.export() 
pwm1.period = 20000000
pwm1.duty_cycle = zeroRot 

pwm0.enable = True
pwm1.enable = True

if not debug:
    print("waiting for motor")
    sleep(3)
    print("motor ready")

speed = 1200000

if debug:
    speed = minSpeed

pwm0.duty_cycle = speed

camera = PiCamera()

try:
    rawCapture = PiYUVArray(camera)
    stream = camera.capture_continuous(rawCapture, format="yuv", use_video_port=True)
    for frame in stream:
        I = frame.array[:, :, 0]
        rawCapture.truncate(0)
        mid_vertical = int(I.shape[1]/2)
        mid_horizontal = [int(I.shape[0]*0.25),int(I.shape[0]*0.50),int(I.shape[0]*0.75)]
        
        
        pre=[]
        for l in mid_horizontal:
            L = I[l, :]
                                                 
            Lf = filtfilt(b, a, l)
        
        # normalize LF
            max_Lf = max(Lf)
            min_Lf = min(Lf)
            Lf = [val/(max_Lf - min_Lf) for val in Lf]
        
            p = find_peaks(Lf, 0.9)
        
            closest_peak_at = -1
            distance_peak = 1000000
            for peak in p[0]:
                if abs(mid_vertical - peak) < distance_peak:
                    closest_peak_at = peak
                    distance_peak = abs(mid_vertical - peak)
            deviation = ((mid_vertical - closest_peak_at)*1.0)/mid_vertical
            threshold_deviation = 0.15
            if deviation < -1*threshold_deviation:
                print("go right")
                pre.append("right")
                #move = "right"
            elif -1*threshold_deviation <= deviation <= threshold_deviation:
                speed=speed*1.10
                print("go straight")
                pre.append("straight")
                #move = "straight"
            else:
                print("go left")
                pre.append("left")
                #move = "left"
        
        if debug:
            print("""
                peaks: {0}
                closest_peak_at: {1}
                deviation: {2}
                threshold_deviation: {3}
                result:{4}
            """.format(str(p[0]), closest_peak_at, deviation, threshold_deviation, move))
            continue
        if(pre[0]==pre[1]==pre[2]=="straight"):
            move="accelerate"
        elif(pre[0]==pre[1]==pre[2]=="left"):
            move="hard left"
        elif(pre[0]==pre[1]==pre[2]=="right"):
            move="hard right"
        elif(pre[0]!=pre[1] and pre[0]==pre[2]):
            move=pre[0]
        else:
            move=pre[0]
            
        if move == 'hard left':
            speed=speed*0.8
            rot = min(zeroRot + maxRot, rot+0.10*rot)
        elif move == 'hard right':
            speed=speed*0.8
            rot = max(zeroRot -maxRot, rot-0.10*rot)
        elif move=="accelerate":
            speed=speed*1.25
        elif move == 'left':
            #speed=speed*0.8
            rot = max(zeroRot -maxRot, rot+0.10*rot)
        elif move == 'right':
            #speed=speed*0.8
            rot = max(zeroRot -maxRot, rot-0.10*rot)
        else:
            rot = zeroRot

        pwm1.duty_cycle = int(rot)
except (KeyboardInterrupt, SystemExit):
    # bring the car on rest in any system failure
    pwm0.duty_cycle = minSpeed
    pwm1.duty_cycle = zeroRot
    stream.close()
    rawCapture.close()
    camera.close()
except Exception as e:
    pwm0.duty_cycle = minSpeed
    pwm1.duty_cycle = zeroRot
    stream.close()
    rawCapture.close()
    camera.close()
