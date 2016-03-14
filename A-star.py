import cv2
import numpy as np
import copy
import glob
import math
import Queue as Q
import time

class pixel(object):
    def __init__(self, penalty, pointx, pointy, parent, h): # parent is that pixel from which this current pixel is generated
        self.penalty = penalty
        self.pointx = int(pointx)
        self.pointy = int(pointy)
        self.parent = parent
        self.h = h #heuristic

    def __cmp__(self, other): # comparable which will return self.penalty<other.penalty
        return cmp(self.penalty+self.h, other.penalty+other.h)

images = glob.glob('*.jpg')

def feasibility(nx, ny, img):  # function to check if pixel lies in obstacle
    if img[nx, ny, 0] == 255:
        return False
    else:
        return True

def penalty(ox, oy, nx, ny, penalty): #ox, oy:- old points  nx, ny :- new points
    return penalty + math.sqrt((ox-nx)*(ox-nx)+ (oy-ny)*(oy-ny))

def heuristic(nx, ny,dx, dy): #ox, oy:- old points  nx, ny :- new points
    return math.sqrt((nx-dx)*(nx-dx)+ (ny-dy)*(ny-dy))


def check_boundaries(ex, ey, nx, ny): #ex, ey :- end points of frame
    if nx > -1 and ny > -1 and nx < ex and ny < ey:
        return True
    else:
        return False

def bfs(arr, sx, sy, dx, dy, final_contours): # sx, sy :- source coordinates  dx, dy :- destination coordinates
    q = Q.PriorityQueue()
    temp1 = True
    temp2 = True

    for cnt in final_contours:
        if cv2.pointPolygonTest(cnt, (sx, sy), False) > -1:
            temp1 = False

    for cnt in final_contours:
        if cv2.pointPolygonTest(cnt, (dx, dy), False) > -1:
            temp2 = False

    if temp1 == False or temp2 == False:
        return []

    actions = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    solution = []
    ex, ey, ez = arr.shape
    #visit = [[False for x in range(ey)] for x in range(ex)]
    dist = [[10000 for x in range(ey)] for x in range(ex)]
    distplusHeuristic = [[10000 for x in range(ey)] for x in range(ex)]

    q.put(pixel(0, sx, sy, None, heuristic(sx, sy, dx, dy)))
    dist[sx][sy] = 0
    distplusHeuristic[sx][sy] = dist[sx][sy]+heuristic(sx, sy, dx, dy)
    s = time.clock()
    cnt = 0
    cntq = 0
    while not q.empty():
        p = q.get()
        x = int(p.pointx)
        y = int(p.pointy)
        pen = p.penalty
        h = p.h
        cnt = cnt+1
        if dist[x][y] < pen:
            continue
        if x == dx and y == dy:
            while p is not None:
                solution.append([p.pointx, p.pointy])
                p = p.parent
            print 'time : ', time.clock()-s
            print cnt, cntq
            return solution

        for i in range(len(actions)):
            nx = int(actions[i][0] + x)
            ny = int(actions[i][1] + y)
            if check_boundaries(ex, ey, nx, ny) == True:
                if arr.item(nx, ny, 0) == 0 and arr.item(nx, ny, 1) == 0 and arr.item(nx, ny, 2) == 0:
                    pen = dist[x][y]
                    pen_new = penalty(x, y, nx, ny, pen)
                    h_new = heuristic(nx, ny, dx, dy)
                    if dist[nx][ny] > pen_new :
                        dist[nx][ny]  = pen_new
                        nx = int(nx)
                        ny = int(ny)
                    if distplusHeuristic[nx][ny] > dist[nx][ny]+h_new :
                        distplusHeuristic[nx][ny] = dist[nx][ny] + h_new
                        cntq = cntq+1
                        q.put(pixel(pen_new, nx, ny, p, h_new))
    print 'time : ', time.clock()-s
    return []

def main():
    counter = 1
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

        output = 'beforeplanningwithoutclearance/' + `counter`
        output += ".jpg"
        cv2.imwrite(output, arr)
        sx = 20 # raw_input("Enter source and destination Coordinates")
        sy = 20  # raw_input()
        dx = 190   # raw_input()
        dy = 190  # raw_input()

       # s = time.clock()
        solution = bfs(arr, sx, sy, dx, dy, final_contours)
      #  print 'time: ', time.clock()-s
        if len(solution) == 0:
            print 'No solution from source to destination'
        else:
            for i in range(len(solution)):
                start = (solution[i][1], solution[i][0])
                cv2.circle(arr,start, 1, [255, 0, 255])
                cv2.circle(img, start, 1, [255, 255, 255])
        output = "withoutClearance/"+`counter`
        output += ".jpg"
        cv2.imwrite(output, img)
        counter += 1
        cv2.circle(arr, (sy, sx), 2, [0, 255, 0])
        cv2.circle(arr, (dy, dx), 2, [0, 255, 0])
        cv2.circle(img, (sy, sx), 2, [0, 255, 0])
        cv2.circle(img, (dy, dx), 2, [0, 255, 0])
        cv2.imshow('image', img)
        cv2.imshow('arr', arr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

main()