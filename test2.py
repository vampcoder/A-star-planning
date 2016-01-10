import cv2
import numpy as np
import copy
import time
from datetime import datetime



cap = cv2.VideoCapture(1)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('AFTER HSV FILTERING')

# Starting with 100's to prevent error while masking
h,s,v = 110,40,0

# Creating track bar
cv2.createTrackbar('h', 'AFTER HSV FILTERING',0,179,nothing)
cv2.createTrackbar('s', 'AFTER HSV FILTERING',0,255,nothing)
cv2.createTrackbar('v', 'AFTER HSV FILTERING',0,255,nothing)

while(1):
#    time.sleep(0.2)
    _, frame = cap.read()
    frame1 = copy.copy(frame)

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','AFTER HSV FILTERING')
    s = cv2.getTrackbarPos('s','AFTER HSV FILTERING')
    v = cv2.getTrackbarPos('v','AFTER HSV FILTERING')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h + 20,s + 140,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)
    blur = cv2.blur(result,(5,5))

    bw = cv2.cvtColor(blur,cv2.COLOR_HSV2BGR)
    bw2 = cv2.cvtColor(bw,cv2.COLOR_BGR2GRAY)

    th3 = cv2.adaptiveThreshold(bw2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    #edges = cv2.Canny(th3,100,200)
    th4 = copy.copy(th3)



    image, contours, hierarchy = cv2.findContours(th4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print len(contours)
    cv2.imshow('AFTER HSV FILTERING',blur)
    cv2.imshow('REAL IMAGE',image)
    cv2.imshow('FINAL IMAGE AFTER THRESHOLDING',th3)
    #cnt = contours[4]
   # perimeter = 0
    #j = 0;
    #for i in xrange(len(contours)):
     #   if(perimeter < cv2.arcLength(contours[i], True)):
      #      perimeter = cv2.arcLength(contours[i], True)
       #     j = i;
    epsilon = 0.1*cv2.arcLength(contours,True)
    approx = cv2.approxPolyDP(contours,epsilon,True)
    cv2.drawContours(frame1, epsilon, -1, (0, 255, 0), 3)
    cv2.imshow('Countours', frame1)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()