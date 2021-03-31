import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon
import random


def line(x1, y1, x2, y2, cl='y'):
    x_values = [x1, x2]
    y_values = [y1, y2]
    plt.plot(x_values, y_values, color=cl)


def findpoint(x1, y1, x2, y2, stepd):
    p = Point(x1, y1)
    c = p.buffer(stepd).boundary
    l = LineString([(x1, y1), (x2, y2)])
    i = c.intersection(l)
    return i.coords[0]


def nearest(x1, y1, pts):
    min = 10000
    temp = ()
    for i in pts:
        l = ((i[0]-x1)**2+(i[1]-y1)**2)**0.5
        if l < min:
            temp = i
            min = l
    return temp


def RRT(start, gl, obstacle_list):

    polys = [Polygon(i) for i in obstacle_list]
    start = (start[0], start[1], None, None)
    pt = Point(gl[0], gl[1])
    buffer = 1
    goal = pt.buffer(buffer)
    stepd = 0.5
    nodes = 10000
    path = []
    pts = [start]

    for i in range(nodes):
        r1 = round(random.uniform(0, 10), 2)
        r2 = round(random.uniform(0, 10), 2)
        nrst = nearest(r1, r2, pts)
        try:
            x, y = findpoint(nrst[0], nrst[1], r1, r2, stepd)
        except:
            continue
        x = round(x, 2)
        y = round(y, 2)
        temp = Point(x, y)
        l = LineString([(x, y), (nrst[0], nrst[1])])
        brk = False
        for k in polys:
            if k.intersection(l):
                brk = True
                break
        if brk:
            continue
        pts.append((x, y, nrst[0], nrst[1]))

        if temp.within(goal):
            pts.append((gl[0], gl[1], x, y))
            #path = [(gl[0], gl[1], x, y)]
            t1, t2 = gl[0], gl[1]
            while (t1, t2) != (start[0], start[1]):
                for j in pts:
                    if (j[0], j[1]) == (t1, t2):
                        path.append(j)
                        t1, t2 = j[2], j[3]
            break
    return path


def visualise(path, obstacle_list):

    for j in obstacle_list:
        for i in range(len(j)):
            try:
                line(j[i][0], j[i][1], j[i+1][0], j[i+1][1], 'r')
            except:
                line(j[i][0], j[i][1], j[0][0], j[0][1], 'r')
    plt.plot(path[0][0], path[0][1], 'ro')
    for j in path:
        try:
            line(j[0], j[1], j[2], j[3], 'g')
        except:
            pass
    plt.show()


if __name__ == "__main__":
    ol = [
        [(2, 10), (7, 10), (6, 7), (4, 7), (4, 9), (2, 9)],
        [(3, 1), (3, 6), (4, 6), (4, 1)],
        [(7, 3), (7, 8), (9, 8), (9, 3)],
    ]

    path = RRT((0, 0), (10, 10), ol)
    visualise(path, ol)
