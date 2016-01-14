import cv2
import numpy as np
import copy
import glob
import math
import time
import Queue as Q


class pixel(object):
    def __init__(self, penalty, pointx, pointy): # parent is that pixel from which this current pixel is generated
        self.penalty = penalty
        self.pointx = int(pointx)
        self.pointy = int(pointy)

    def __cmp__(self, other): # comparable which will return self.penalty<other.penalty
        return cmp(self.penalty, other.penalty)

images = glob.glob('*.jpg')


def penalty(ox, oy, nx, ny, penalty): #ox, oy:- old points  nx, ny :- new points
    return penalty + math.sqrt((ox-nx)*(ox-nx)+ (oy-ny)*(oy-ny))


def check_boundaries(ex, ey, nx, ny): #ex, ey :- end points of frame
    if nx > -1 and ny > -1 and nx < ex and ny < ey:
        return True
    else:
        return False


def fill_clearance(arr,cmax,  final_contours): # sx, sy :- source coordinates  dx, dy :- destination coordinates
    q = Q.PriorityQueue()

    actions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    ex, ey, ez = arr.shape
    #print ex, ey, ez
    min_cost = [[100000 for x in range(ey)] for x in range(ex)]
    for cnt in final_contours:
        for pts in cnt:
            q.put(pixel(0, pts[0, 1], pts[0, 0]))
    cnt = 0
    cntq = 0
    while not q.empty():
        p = q.get()
        x = int(p.pointx)
        y = int(p.pointy)
        pen = p.penalty
        if p.penalty > cmax:
            continue
        if min_cost[x][y] <= p.penalty:
            continue
        min_cost[x][y] = p.penalty

        for i in range(len(actions)):
            nx = int(actions[i][0] + x)
            ny = int(actions[i][1] + y)
            if check_boundaries(ex, ey, nx, ny) == True:
                if arr.item(nx, ny, 0) == 0 and arr.item(nx, ny, 1) == 0 and arr.item(nx, ny, 2) == 0:
                    if min_cost[nx][ny] > penalty(x, y, nx, ny, pen):
                        q.put(pixel(penalty(x,y,nx,ny,pen), nx, ny))
    return min_cost


def main():
    for im in images:

        img = cv2.imread(im)

        cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img2 = cv2.medianBlur(cimg,13)

        ret,thresh1 = cv2.threshold(cimg,40,255,cv2.THRESH_BINARY)
        t2 = copy.copy(thresh1)

        x, y  = thresh1.shape
        arr = np.zeros((x, y, 3), np.uint8)
        final_contours= []
        image, contours, hierarchy = cv2.findContours(t2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            cnt = contours[i]
            if cv2.contourArea(cnt) > 300 and cv2.contourArea(cnt) < 5000 :
                cv2.drawContours(img, [cnt],-1, [0, 255, 255])
                cv2.fillConvexPoly(arr, cnt, [255, 255, 255])
                final_contours.append(cnt)
        cmax = 50
        start = time.clock()
        min_cost = fill_clearance(arr,cmax, final_contours)
        print 'time: ',  time.clock()-start
        for i in xrange(x):
            for j in xrange(y):
                pix_val = int(255-4*min_cost[i][j])
                if(min_cost[i][j] > 10000):
                    pix_val = 0
                arr[i, j] = (pix_val, pix_val, pix_val)
        for cnt in final_contours:
            cv2.fillConvexPoly(arr, cnt, [255, 255, 255])

        cv2.imshow('image', img)
        cv2.imshow('arr', arr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


main()