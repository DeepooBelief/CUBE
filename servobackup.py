import RPi.GPIO as GPIO
import time
pin = 7
GPIO.setmode(GPIO.BOARD)
# GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)
p = GPIO.PWM(pin,50)
p.start(0)
Original_angle = 16.2
Flip_angle = 45

def delay(t):
    #delay in milli seconds
    start, end = 0,0
    start = time.time()
    t = (t - 5) /1000
    while end - start < t:
        end = time.time()
        
def servo(angle):
    i = angle/18+2.5
    global p
    print(i)
    p.ChangeDutyCycle(i)
    time.sleep(0.015)

servo(120)
#servo(Flip_angle)
#print("flip angle finished")
#delay(100)
#servo(Original_angle)
#print("return to original angle")
#servo(0)

p.stop()
GPIO.cleanup()

