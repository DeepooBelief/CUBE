import cv2 as cv
import time

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    c = cv.waitKey(1)
    time.sleep(0.033)
    if c == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        exit()
    # cv.namedWindow("frame", 0)
    cv.imshow('frame', frame)
