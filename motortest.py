import RPi.GPIO as GPIO
import time
RESOLUTION = 2
# 方向引脚
dir_pin = 17

# 步进引脚
step_pin = 27

sleep_pin = 22
# 电机每圈步数
STEPS_PER_REV = 200

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BCM)

# 设置引脚为输出模式
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(step_pin, GPIO.OUT)
GPIO.setup(sleep_pin, GPIO.OUT)
GPIO.output(sleep_pin, GPIO.HIGH)


def rotate_Angle(angle=90, clockwise=True, speed=0.0005):
    # 设置电机方向
    GPIO.output(dir_pin, clockwise)

    # 电机旋转
    for x in range((STEPS_PER_REV * angle * RESOLUTION)//360):
        GPIO.output(step_pin, GPIO.HIGH)
        time.sleep(speed)
        GPIO.output(step_pin, GPIO.LOW)
        time.sleep(speed)
        #print(x)


rotate_Angle(angle=180, clockwise=False, speed=0.0009)

# 等待一秒钟
time.sleep(1)

# 清理GPIO引脚设置
GPIO.cleanup()