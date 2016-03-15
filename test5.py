import cv2
import numpy as np
import copy
import glob

images = glob.glob('*.jpg')

for im in images:
    img = cv2.imread(im)

    cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img2 = cv2.medianBlur(cimg,13)

    ret,thresh1 = cv2.threshold(cimg,100,120,cv2.THRESH_BINARY)
    t2 = copy.copy(thresh1)
    th3 = cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    image, contours, hierarchy = cv2.findContours(t2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (0,255,0), 3)

    for i in xrange(len(contours)):
        cnt = contours[i]
        if cv2.contourArea(cnt) > 1000 and cv2.contourArea(cnt) < 15000:
            cv2.drawContours(img, [cnt],-1, [255, 255, 255])
        '''
        if cv2.contourArea(cnt) > 0  and cv2.contourArea(cnt) < 10000000:
            hull = cv2.convexHull(cnt,returnPoints = False)
            defects = cv2.convexityDefects(cnt,hull)

            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                cv2.line(img,start,end,[0,255,0],1)
        '''

    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()