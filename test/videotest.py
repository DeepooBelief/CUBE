import cv2 as cv
import time

color = 'orange'
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
cap.set(3, 640)
cap.set(4, 480)

ret, frame = cap.read()
    
def get_hsv(event, x, y, flags, param):
    global frame
    if event == cv.EVENT_LBUTTONDOWN:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        print("HSV:", hsv[y, x])
        print("{},{},{},{}".format(color, hsv[y, x][0] * 2, hsv[y, x][1] / 2.55, hsv[y, x][2] / 2.55))
        with open('color.csv', "a") as f:
           f.write("{},{},{},{}\r".format(color, int(hsv[y, x][0] * 2), int(hsv[y, x][1] / 2.55), int(hsv[y, x][2] / 2.55)))
  
def main():
    global frame
    cv.namedWindow('frame')
    cv.setMouseCallback("frame", get_hsv)
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

if __name__ == "__main__":
    main()