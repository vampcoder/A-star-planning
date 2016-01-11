import cv2
import numpy as np
import copy
import glob
import math
import time

def distance (one, point) :
    dist = math.hypot(point[0] - one[0], point[1] - one[1])
    return dist

def distFromContour (one, two, point):
    y = two[1]-one[1]
    x = two[0]-one[0]
    vec = np.array([x,y,0])
    p1 = np.array([point[0]-one[0],point[1]-one[1],0])
    p2 = np.array([point[0]-two[0],point[1]-two[1],0])
    pro1 = np.dot(vec,p1)
    pro2 = np.dot(vec,p2)
    if pro1 > 0 and pro2 > 0 :
        return min(distance(one,point),distance(two,point))
    elif pro1 < 0 and pro2 < 0:
        return min(distance(one,point),distance(two,point))
    elif pro1 <= 0 or pro2 <= 0:
        result = (point[0]*y - point[1]*x + one[1]*x - one[0]*y)/((x**2 + y**2)**0.5)
        if result < 0 :
            result *= -1
        return result


images = glob.glob('*.jpg')

for im in images:
    img = cv2.imread(im)

    cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img2 = cv2.medianBlur(cimg,13)

    ret,thresh1 = cv2.threshold(cimg,40,255,cv2.THRESH_BINARY)
    t2 = copy.copy(thresh1)
    image, contours, hierarchy = cv2.findContours(t2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (0,255,0), 3)

    x, y  = thresh1.shape
    final_contours = []
  #  print x, y
    for i in range(len(contours)):
        cnt = contours[i]
        if cv2.contourArea(cnt) > 300 and cv2.contourArea(cnt) < 5000:
            final_contours.append(cnt)
    arr = np.zeros((x, y, 3), np.uint8)
   # print arr.shape
   # finalarr = [[10000 for p in range(y)] for p in range(x)]
    finalimg = np.zeros((x, y, 3), np.uint8)
   # print finalimg.shape
  #  print len(finalarr)
    max_dist = 0
    s = time.clock()
    for j in xrange(x):
        for k in xrange(y):
            dist = 1000
            for i in range(len(final_contours)):
                cnt = final_contours[i]
                hull = cv2.convexHull(cnt, clockwise=True, returnPoints= True)
                #print len(hull)
                cv2.fillConvexPoly(arr, hull, [255, 255, 255])
                for i in range(len(hull)):
                   # print hull[i]
                    start = tuple(hull[i, 0])
                    end = tuple(hull[(i+1) % len(hull), 0])
                    cv2.line(img, start, end, [0, 255, 0], 1)

                    val = distFromContour(start,end,[k,j])
                    if val < dist:
                        dist = val
            if dist > max_dist:
                max_dist = dist
                print max_dist
            if arr[j][k][0] != 255:
                finalimg[j][k] = (round(dist * 0.8), round(dist * 0.8), round(dist * 0.8))
    print 'time: ', time.clock()-s

    print max_dist
    cv2.imshow('image',img)
    cv2.imshow('image2', arr)
#    image = np.zeros((x, y,3), np.uint8)

    cv2.imshow('imag',finalimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()