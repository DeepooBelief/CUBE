import RPi.GPIO as GPIO
import time

dirPin = 2
stepPin = 3
sleepPin = 4
MOTOR_STEPS = 200
resolution = 2
periods = 1000

cube_pos = ["U", "D", "F", "B", "L", "R"]

def delayMicrosecond(t):
    start, end = 0,0
    start = time.time()
    t = (t - 5) /1000000
    while end - start < t:
        end = time.time()

def initStepper():
    GPIO.setup(stepPin, GPIO.OUT)
    GPIO.setup(sleepPin, GPIO.OUT)
    GPIO.setup(dirPin, GPIO.OUT)


def rotateArg(angle, period, anti):
    GPIO.output(dirPin, anti)
    for i in range(angle * MOTOR_STEPS * resolution // 360):
        GPIO.output(stepPin, True)
        delayMicrosecond(period)
        GPIO.output(stepPin, False)
        delayMicrosecond(period)
        print(i)


def swap(a, b):
    a, b = b, a


def movement_y(a):
    print("y rotate")
    rotateArg(90, periods, True)
    swap(a[2], a[5])
    swap(a[3], a[4])
    swap(a[4], a[5])


def movement_y_ivt(a):
    print("y_ivt rotate")
    rotateArg(90, periods, False)
    swap(a[2], a[4])
    swap(a[3], a[4])
    swap(a[3], a[5])


def movement_x(a):
    print("x rotate")
    input()
    swap(a[0], a[2])
    swap(a[1], a[2])
    swap(a[1], a[3])


def movement_x_ivt(a):
    print("x_ivt rotate")
    input()
    swap(a[0], a[3])
    swap(a[3], a[2])
    swap(a[1], a[3])


def to_U(a):
    movement_x(a)
    movement_x(a)


def to_F(a):
    movement_x_ivt(a)


def to_B(a):
    movement_x(a)


def to_L(a):
    movement_y_ivt(a)
    movement_x_ivt(a)


def to_R(a):
    movement_y(a)
    movement_x_ivt(a)


def to_D(a):
    pass

p = [to_U, to_D, to_F, to_B, to_L, to_R]

def manipulateCube(res):
    for c in res:
        if c.isalpha():
            j = 0
            while cube_pos[j] != c:
                j += 1
            p[j](cube_pos)
        elif c.isdigit():
            print("Lock")
            input()
            rotateArg(90*int(c), periods, False);
            print('Unlock')
            input()

GPIO.setmode(GPIO.BCM)
initStepper()
GPIO.output(sleepPin, True)
manipulateCube('F2')
GPIO.output(sleepPin, False)
GPIO.cleanup()
