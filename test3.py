import cv2
import numpy as np
import copy
import time



cap = cv2.VideoCapture(0)
h1 = 10
s1 = 140
v1 = 0
def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('AFTER HSV FILTERING')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'AFTER HSV FILTERING',0,179-h1,nothing)
cv2.createTrackbar('s', 'AFTER HSV FILTERING',0,255-s1,nothing)
cv2.createTrackbar('v', 'AFTER HSV FILTERING',0,255-v1,nothing)


while(1):
    time.sleep(0.1)
    _, frame = cap.read()

    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','AFTER HSV FILTERING')
    s = cv2.getTrackbarPos('s','AFTER HSV FILTERING')
    v = cv2.getTrackbarPos('v','AFTER HSV FILTERING')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([h + h1,s + s1,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)
    blur = cv2.blur(result,(5,5))

    bw = cv2.cvtColor(blur,cv2.COLOR_HSV2BGR)
    bw2 = cv2.cvtColor(bw,cv2.COLOR_BGR2GRAY)
    ret,th3 = cv2.threshold(bw2,30,255,cv2.THRESH_BINARY)
    #th3 = cv2.adaptiveThreshold(bw2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            #cv2.THRESH_BINARY,11,2)
    edges = cv2.Canny(th3,100,200)
    th4 = copy.copy(th3)

    perimeter = 0
    j = 0
    image, contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
   # print len(contours)
   # if(len(contours) > 5):
    #    continue
    cnt = np.array([])
    for i in range(len(contours)):
        if(perimeter < cv2.contourArea(contours[i])):
            perimeter = cv2.contourArea(contours[i])
            j = i;
            cnt = contours[j]
    if(len(cnt) == 0):
        continue
    cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
    #ellipse = cv2.fitEllipse(cnt)
    #frame = cv2.ellipse(frame,ellipse,(0,0,255),2)

    #(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
    #print angle

    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    d1 = 0
    p1 = []

    s,e,f,d = defects[0,0]
    start = tuple(cnt[s][0])
    cv2.circle(frame, start, 5, [255, 0, 0], -1)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        dist = d
        if dist > d1:
            d1 = dist
            p1 = far
        cv2.line(frame,start,end,[0,0,0],2)
        
    if len(p1)> 0:
        cv2.circle(frame, p1, 5, [0, 255, 255], -1)

    #draw end points

    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    cv2.circle(frame, leftmost, 5, [0,0, 255], -1)
    cv2.circle(frame, rightmost, 5, [0, 0, 255], -1)
    cv2.circle(frame, bottommost, 5, [0, 0, 255], -1)
    cv2.circle(frame, topmost, 5, [0, 0, 255], -1)
    #cv2.circle(frame, p2, 5, [0, 255, 255], -1)
    cv2.imshow('AFTER HSV FILTERING',blur)
    cv2.imshow('REAL IMAGE',frame)
    cv2.imshow('FINAL IMAGE AFTER THRESHOLDING',bw2)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()