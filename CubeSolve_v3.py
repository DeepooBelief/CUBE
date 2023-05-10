import numpy as np
import cv2 as cv
import colorsys
import csv
import time
from ctypes import *


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
cap.set(3, 640)
cap.set(4, 480)

ptLT = (85,20)
LineColour = {'red': (0,0,255), 'orange': (0, 127, 255), 'yellow': (0, 255, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'white': (255, 255, 255)}
cube_color = [[0]*9 for i in range(6)]
Color2Pos = {'orange': 'L', 'blue': 'F', 'green': 'B', 'red': 'R', 'yellow': 'U', 'white': 'D'}
Seperation = 172 #摄像头正方形的间距
Length = 80 #摄像头正方形的边长

face_color = [0]*9
order = 'URFDLB'#'UFRBLD'

cube_pos = ["B", "F", "U", "D", "L", "R"]
writeOrder = ['123456789', '123456789', '123456789', '123456789', '123456789', '741852963']
hw = CDLL('./motorservo.dll') #use the dll to control stepper motor and servo
hw.wiringPiSetup() #used to setup pins
hw.motorsetup() #used to setup stepper motor
hw.pwmsetup() #used to setup servo


def drawBlocks(picture, color):
    for i in range(3):
        for j in range(3):
            ptLT_Temp = (ptLT[0] + Seperation*j, ptLT[1] + Seperation*i)
            ptRB_Temp = (ptLT_Temp[0]+Length,ptLT_Temp[1]+Length)
            cv.rectangle(picture, ptLT_Temp, ptRB_Temp, color, 1)

def movement_y(a):
    print("y rotate")
    hw.rotate(90, True)
    a[2], a[5] = a[5], a[2]
    a[3], a[4] = a[4], a[3]
    a[4], a[5] = a[5], a[4]


def movement_y_ivt(a):
    print("y_ivt rotate")
    hw.rotate(90, False)
    a[2], a[4] = a[4], a[2]
    a[3], a[4] = a[4], a[3]
    a[3], a[5] = a[5], a[3]


def movement_x(a):
    print("x rotate")
    hw.flip_cube()
    hw.delay(100)
    a[0], a[2] = a[2], a[0]
    a[1], a[2] = a[2], a[1]
    a[1], a[3] = a[3], a[1]

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
            hw.releasePins()
            break

        drawBlocks(frame, (255, 255, 255))
        cv.imshow('frame', frame)

        c = cv.waitKey(1)
        if c == ord('q'):
            break

        elif c == ord('c'): #'c' means capture the color info, you need to type in the color like "orange", "yellow" etc.
            col = input()
            for i in range(3):
                for j in range(3):
                    ptLT_Temp = (ptLT[0] + Seperation*j, ptLT[1] + Seperation*i)
                    ptRB_Temp = (ptLT_Temp[0]+Length,ptLT_Temp[1]+Length)
                    a = [0, 0, 0]
                    for channel in range(3):
                        a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + Length, ptLT_Temp[0] + 1: ptLT_Temp[0] + Length, channel])

                    (H,S,V) = colorsys.rgb_to_hsv(a[2]/ 255, a[1]/ 255, a[0]/ 255)
                    (H,S,V) = (int(H * 360), int(S * 100), int(V * 100))
                    row = [col, H, S, V]
                    print('H s v:', H,S,V)
                    with open('color.csv', 'a', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)

            f.close()
        elif c == ord('w'):
            movement_x(cube_pos)
        elif c == ord('a'):
            movement_y(cube_pos)
        elif c == ord('d'):
            movement_y_ivt(cube_pos)

    hw.releasePins()
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



def to_U(a):
    movement_x(a)
    movement_x(a)


def to_F(a):
    movement_y(a)
    movement_y(a)
    hw.delay(100)
    movement_x(a)


def to_B(a):
    movement_x(a)


def to_L(a):
    movement_y(a)
    hw.delay(100)
    movement_x(a)


def to_R(a):
    movement_y_ivt(a)
    hw.delay(100)
    movement_x(a)


def to_D(a):
    pass

p = [to_U, to_D, to_F, to_B, to_L, to_R]

def manipulateCube(res):
    for c in res:
        if c.isalpha():
            p[cube_pos.index(c)](cube_pos)
        elif c.isdigit():
            i = int(c)
            hw.lock()
            if i == 3:
                hw.rotate(90, True);
            else:
                hw.rotate(90*int(c), False);
            hw.unlock()
            
def writeColor(face, order):
    for i, c in enumerate(order):
        face[int(c) - 1] = face_color[i]        


face_idx = 0
import twophase.solver  as sv


def my_function():
    global face_color, face_idx
    hw.cam_pos()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        c = cv.waitKey(1)
        if c == ord('q'):
            cap.release()
            cv.destroyAllWindows()
            hw.releasePins()
            exit()
        elif c == ord('s'):
            
            ret, frame = cap.read()
            for i in range(3):
                for j in range(3):
                    ptLT_Temp = (ptLT[0] + Seperation*j, ptLT[1] + Seperation*i)
                    ptRB_Temp = (ptLT_Temp[0]+Length,ptLT_Temp[1]+Length)
                    a = [0, 0, 0]
                    for channel in range(3):
                        a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + Length, ptLT_Temp[0] + 1: ptLT_Temp[0] + Length, channel])

                    (H,S,V) = colorsys.rgb_to_hsv(a[2]/ 255, a[1]/ 255, a[0]/ 255)
                    (H,S,V) = (int(H * 360), int(S * 100), int(V * 100))
                    HSV = {'H': H, 'S': S, 'V': V}
                    color = knn(HSV)
                    if HSV['S'] < 20:
                        color = 'white'
                    
                    face_color[i * 3 + j] = color
                    cv.rectangle(frame, ptLT_Temp, ptRB_Temp, LineColour[color], 2)
            SCAN_ORDER = "UFRBLD"
            #for idx in range(9):
                #cube_color[face_idx][idx] = face_color[idx]
            writeColor(cube_color[order.find(SCAN_ORDER[face_idx])], writeOrder[face_idx])
            Color2Pos[face_color[4]] = SCAN_ORDER[face_idx]
            print(cube_color)
            print(Color2Pos)
            #input()
            hw.unlock()
            print("unlock")
            if face_idx == 5:
                break
            if face_idx == 0 or face_idx == 4:
                movement_x(cube_pos)
            else:
                movement_y(cube_pos)
            face_idx += 1
            hw.cam_pos()
            print("cam pos")
            cv.imshow('frame', frame)
            #manipulateCube(order[face_idx - 3])
    
        for i in range(3):
            for j in range(3):
                ptLT_Temp = (ptLT[0] + Seperation*j, ptLT[1] + Seperation*i)
                ptRB_Temp = (ptLT_Temp[0]+Length,ptLT_Temp[1]+Length)
                a = [0, 0, 0]
                for channel in range(3):
                    a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + Length, ptLT_Temp[0] + 1: ptLT_Temp[0] + Length, channel])

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
        
    hw.releasePins()
    cap.release()
    cv.destroyAllWindows()

my_function()
