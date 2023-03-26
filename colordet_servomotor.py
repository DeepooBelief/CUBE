import numpy as np
import cv2 as cv
import colorsys
import csv
from Servomotor import *

cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

ptLT = (50,40)
LineColour = {'red': (0,0,255), 'orange': (0, 127, 255), 'yellow': (0, 255, 255), 'green': (0, 255, 0), 'blue': (255, 0, 0), 'white': (255, 255, 255)}

def drawBlocks(picture, color):
    for i in range(3):
        for j in range(3):
            ptLT_Temp = (ptLT[0] + 170*j, ptLT[1] + 170*i)
            ptRB_Temp = (ptLT_Temp[0]+90,ptLT_Temp[1]+90)
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
                    ptLT_Temp = (ptLT[0] + 170*j, ptLT[1] + 170*i)
                    ptRB_Temp = (ptLT_Temp[0]+90,ptLT_Temp[1]+90)
                    a = [0, 0, 0]
                    for channel in range(3):
                        a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + 90, ptLT_Temp[0] + 1: ptLT_Temp[0] + 90, channel])
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

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    c = cv.waitKey(1)
    if c == ord('q'):
        break
    
    for i in range(3):
        for j in range(3):
            ptLT_Temp = (ptLT[0] + 170*j, ptLT[1] + 170*i)
            ptRB_Temp = (ptLT_Temp[0]+90,ptLT_Temp[1]+90)
            a = [0, 0, 0]
            for channel in range(3):
                a[channel] = np.mean(frame[ptLT_Temp[1] + 1 : ptLT_Temp[1] + 90, ptLT_Temp[0] + 1: ptLT_Temp[0] + 90, channel])

            (H,S,V) = colorsys.rgb_to_hsv(a[2]/ 255, a[1]/ 255, a[0]/ 255)
            (H,S,V) = (int(H * 360), int(S * 100), int(V * 100))
            HSV = {'H': H, 'S': S, 'V': V}
            color = knn(HSV)
            if HSV['S'] < 35:
                color = 'white'
            cv.rectangle(frame, ptLT_Temp, ptRB_Temp, LineColour[color], 2)

    cv.imshow('frame', frame)

cap.release()
cv.destroyAllWindows()
