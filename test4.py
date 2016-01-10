import cv2
import numpy as np
import copy
import time
import math

cap = cv2.VideoCapture(1)
h1 = 10
s1 = 140
v1 = 0
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('AFTER HSV FILTERING')

h,s,v = 103,40,50

while(1):
    time.sleep(0.5)
    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h + h1,s + s1,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)
    blur = cv2.blur(result,(5,5))

    bw = cv2.cvtColor(blur,cv2.COLOR_HSV2BGR)
    bw2 = cv2.cvtColor(bw,cv2.COLOR_BGR2GRAY)
    ret,th3 = cv2.threshold(bw2,30,255,cv2.THRESH_BINARY)

    edges = cv2.Canny(th3,100,200)
    th4 = copy.copy(th3)

    perimeter = 0
    j = 0
    image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    cnt = np.array([])
    for i in range(len(contours)):
        if(perimeter < cv2.contourArea(contours[i])):
            perimeter = cv2.contourArea(contours[i])
            j = i;
            cnt = contours[j]

    (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)


    hull = cv2.convexHull(cnt)
    avgx, avgy= 0,0
    for pts in hull:
        avgx += pts.item(0)
        avgy += pts.item(1)
    avgx /= len(hull)
    avgy /= len(hull)

    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    t = (cx, cy)
    a = (avgx, avgy)
    cv2.circle(frame, t, 5, [0, 0, 255], -1)
    cv2.circle(frame, a, 5, [255, 0, 0], -1)
    cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

    cv2.imshow('AFTER HSV FILTERING',blur)
    cv2.imshow('REAL IMAGE',frame)
    cv2.imshow('FINAL IMAGE AFTER THRESHOLDING',bw2)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()