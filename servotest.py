import RPi.GPIO as GPIO
import time
Servo_pin = 10
GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
GPIO.setup(Servo_pin,GPIO.OUT)
p = GPIO.PWM(Servo_pin,50)
p.start(2.6)
time.sleep(0.1)

for j in range(10):
    i = 4.4
    p.ChangeDutyCycle(i)
    time.sleep(0.3)

    while i >= 3.1:
        i -= 0.1
        p.ChangeDutyCycle(i)
        time.sleep(0.02)
        

    p.ChangeDutyCycle(2.6)
    time.sleep(0.5)
#i = 0
#while i <= 10:
    #p.ChangeDutyCycle(3.2) #通过输入不同的"占空比值"来观察舵机的位置变化
    #time.sleep(1)
    #p.ChangeDutyCycle(5) #通过输入不同的"占空比值"来观察舵机的位置变化
    #time.sleep(1)
    #i += 1
    
#p.ChangeDutyCycle(3.2)
time.sleep(1)
p.stop()
GPIO.cleanup()
