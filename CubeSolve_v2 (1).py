import numpy as np
import cv2 as cv
import colorsys
import csv
import RPi.GPIO as GPIO
import time

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
cap.set(3, 640)
cap.set(4, 480)

ptLT = (160,85)
LineColour = {'red': (0,0,255), 'orange': (0, 127, 255), 'yellow': (0, 255, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'white': (255, 255, 255)}
cube_color = [[0]*9 for i in range(6)]
Color2Pos = {'orange': 'L', 'blue': 'F', 'green': 'B', 'red': 'R', 'yellow': 'U', 'white': 'D'}

dirPin = 2
stepPin = 3
sleepPin = 4
MOTOR_STEPS = 200
resolution = 2
periods = 1000

face_color = [0]*9
order = 'URFDLB'

cube_pos = ["U", "D", "F", "B", "L", "R"]
writeOrder = ['123456789', '987654321', '741852963', '987654321', '123456789', '741852963']

def drawBlocks(picture, color):
    for i in range(3):
        for j in range(3):
            ptLT_Temp = (ptLT[0] + 115*j, ptLT[1] + 115*i)
            ptRB_Temp = (ptLT_Temp[0]+65,ptLT_Temp[1]+65)
            cv.rectangle(picture, ptLT_Temp, ptRB_Temp, color, 1)

try:
    with open('color.csv', 'r') as f:
        reader = csv.DictReader(f)
        datas = [row for row in reader]

    f.close()
except (FileNotFoundError):
    b = []
    headers = ['Color', 'H', 'S', 'V']
    with open('color.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

    f.close()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        drawBlocks(frame, (255, 255, 255))
        cv.imshow('frame', frame)

        c = cv.waitKey(1)
        if c == ord('q'):
            break

        elif c == ord('c'):
            col = input()
            for i in range(3):
                for j in range(3):
                    ptLT_Temp = (ptLT[0] + 115*j, ptLT[1] + 115*i)
                    ptRB_Temp = (ptLT_Temp[0]+65,ptLT_Temp[1]+65)
                    a = [0, 0, 0]
                    for channel in range(3):
                        a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + 65, ptLT_Temp[0] + 1: ptLT_Temp[0] + 65, channel])
                    b.append(a)

            for i in range(9):
                (H,S,V) = colorsys.rgb_to_hsv(b[-1-i][2]/ 255, b[-1-i][1]/ 255, b[-1-i][0]/ 255)
                (H,S,V) = (int(H * 360), int(S * 100), int(V * 100))
                row = [col, H, S, V]
                print('H s v:', H,S,V)
                with open('color.csv', 'a', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)

            f.close()

    cap.release()
    cv.destroyAllWindows()
    exit()

def distance(d1, d2):
    dH = int(d1['H']) - int(d2['H'])
    if(dH > 180):
        dH-=360
    elif(dH < -180):
        dH+=360
    
    res = dH**2
    for key in ("S","V"):
        res += (int(d1[key]) - int(d2[key]))**2

    return res**0.5

K = 3

def knn(data):
    res = [
        {"result": train['Color'], "distance": distance(data, train)}
        for train in datas
    ]
    
    res = sorted(res, key=lambda item: item['distance'])
    
    res2 = res[0:K]
    
    result = {'red':0, 'orange':0, 'yellow': 0, 'green': 0, 'blue': 0, 'white': 0}
    sum = 0
    for r in res2:
        sum += r['distance']

    for r in res2:
        result[r['result']] += 1 - r['distance']/(sum + 0.1)

    max_val = max(result.values())

    for key, value in result.items():
        if value == max_val:
            return key

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


def movement_y(a):
    print("y rotate")
    rotateArg(90, periods, True)
    a[2], a[5] = a[5], a[2]
    a[3], a[4] = a[4], a[3]
    a[4], a[5] = a[5], a[4]


def movement_y_ivt(a):
    print("y_ivt rotate")
    rotateArg(90, periods, False)
    a[2], a[4] = a[4], a[2]
    a[3], a[4] = a[4], a[3]
    a[3], a[5] = a[5], a[3]


def movement_x(a):
    print("x rotate")
    input()
    a[0], a[2] = a[2], a[0]
    a[1], a[2] = a[2], a[1]
    a[1], a[3] = a[3], a[1]


def movement_x_ivt(a):
    print("x_ivt rotate")
    input()
    a[0], a[3] = a[3], a[0]
    a[3], a[2] = a[2], a[3]
    a[1], a[3] = a[3], a[1]


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
            p[cube_pos.index(c)](cube_pos)
        elif c.isdigit():
            i = int(c)
            print("Lock")
            input()
            if i == 3:
                rotateArg(90, periods, True);
            else:
                rotateArg(90*int(c), periods, False);
            print('Unlock')
            input()
            
def writeColor(face, order):
    for i, c in enumerate(order):
        face[int(c) - 1] = face_color[i]        


face_idx = 0
GPIO.setmode(GPIO.BCM)
initStepper()
GPIO.output(sleepPin,GPIO.HIGH)
import twophase.solver  as sv

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    c = cv.waitKey(1)
    if c == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        GPIO.cleanup()
        exit()
    elif c == ord('s'):
        #for idx in range(9):
            #cube_color[face_idx][idx] = face_color[idx]
        writeColor(cube_color[face_idx], writeOrder[face_idx])
        Color2Pos[face_color[4]] = order[face_idx]
        print(cube_color)
        print(Color2Pos)
        face_idx += 1
        if face_idx == 6:
            break
        manipulateCube(order[face_idx - 3])
    
    for i in range(3):
        for j in range(3):
            ptLT_Temp = (ptLT[0] + 115*j, ptLT[1] + 115*i)
            ptRB_Temp = (ptLT_Temp[0]+65,ptLT_Temp[1]+65)
            a = [0, 0, 0]
            for channel in range(3):
                a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + 65, ptLT_Temp[0] + 1: ptLT_Temp[0] + 65, channel])

            (H,S,V) = colorsys.rgb_to_hsv(a[2]/ 255, a[1]/ 255, a[0]/ 255)
            (H,S,V) = (int(H * 360), int(S * 100), int(V * 100))
            HSV = {'H': H, 'S': S, 'V': V}
            color = knn(HSV)
            if HSV['S'] < 20:
                color = 'white'
            
            face_color[i * 3 + j] = color
            cv.rectangle(frame, ptLT_Temp, ptRB_Temp, LineColour[color], 2)

    cv.imshow('frame', frame)

output = ""
for i in range(6):
    for j in range(9):
        output+=Color2Pos[cube_color[i][j]]

print(output)

result = sv.solve(output,0,2)
print(result)

movs = []
i = 0
while i < len(result)-5:
    c = ""
    if result[i] != ' ':
        c += result[i]
        c += result[i+1]
        movs.append(c)
    i = i+3

for mov in movs:
    print(mov)
    manipulateCube(mov)
    
GPIO.cleanup()
cap.release()
cv.destroyAllWindows()
