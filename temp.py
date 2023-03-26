import cv2 as cv
import numpy as np
#image=cv.imread('inclined.jpg',1)

cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    ret, image = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    c = cv.waitKey(1)
    if c == ord('q'):
        break

    grey = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    ptLT_Temp = (50, 40)
    ptRB_Temp = (500,380)
    roi = cv.rectangle(grey, ptLT_Temp, ptRB_Temp, (255, 255, 255), 1)
    lines1 = cv.HoughLinesP(roi,1,np.pi/180,80,100,70)
    for i in range(len(lines1)):
        x1,y1,x2,y2 = lines1[i][0]
        cv.line(image,(x1,y1),(x2,y2),(0,255,0),2)
    cv.imshow("image",grey)


cap.release()
cv.destroyAllWindows()