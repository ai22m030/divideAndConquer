import math
from enum import Enum


class Orientation(Enum):
    LEFT = 1
    RIGHT = 2
    LINE = 3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw_next = None
        self.ccw_next = None

    def is_left_turn(self, p):
        return (self * p) < 0

    def is_right_turn(self, p):
        return (self * p) > 0

    def is_collinear(self, p):
        return (self * p) == 0

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')\nCW:' \
                '(' + str(self.cw_next.x) + ', ' + str(self.cw_next.y) + ')\nCCW:' \
                '(' + str(self.ccw_next.x) + ', ' + str(self.ccw_next.y) + ')\n'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __mul__(self, p):
        return self.x * p.y - p.x * self.y

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)


def merge(chull1, chull2):
    # get the rightmost point of left convex hull
    p = max(chull1, key=lambda point: point.x)

    # get the leftmost point of right convex hull
    q = min(chull2, key=lambda point: point.x)

    # make copies of p and q
    cp_p = p
    cp_q = q

    # raise the bridge pq to the upper tangent
    while True:
        prev_p = p
        prev_q = q
        if q.cw_next:
            # move p clockwise as long as it makes left turn
            while direction(p, q, q.cw_next) < 0:
                q = q.cw_next
        if p.ccw_next:
            # move p as long as it makes right turn
            while direction(q, p, p.ccw_next) > 0:
                p = p.ccw_next

        if p == prev_p and q == prev_q:
            break

    # lower the bridge cp_p cp_q to the lower tangent
    while True:
        prev_p = cp_p
        prev_q = cp_q
        if cp_q.ccw_next:
            # move q as long as it makes right turn
            while direction(cp_p, cp_q, cp_q.ccw_next) > 0:
                cp_q = cp_q.ccw_next
        if cp_p.cw_next:
            # move p as long as it makes left turn
            while direction(cp_q, cp_p, cp_p.cw_next) < 0:
                cp_p = cp_p.cw_next
        if cp_p == prev_p and cp_q == prev_q:
            break

    # remove all other points
    p.cw_next = q
    q.ccw_next = p

    cp_p.ccw_next = cp_q
    cp_q.cw_next = cp_p

    # final result
    result = []
    start = p
    while True:
        result.append(p)
        p = p.ccw_next

        if p == start:
            break

    return result


def direction(p1, p2, p3):
    # return cross_product(p3.subtract(p1), p2.subtract(p1))
    return (p3 - p1) * (p2 - p1)


def orientation(p_line_1, p_line_2, p_check):
    orient = ((p_line_1.x - p_check.x) * (p_line_2.y - p_check.y)) -\
             ((p_line_1.y - p_check.y) * (p_line_2.x - p_check.x))

    if orient > 0:
        return Orientation.LEFT
    elif orient < 0:
        return Orientation.RIGHT
    else:
        return Orientation.LINE


def collinear(p1, p2, p3):
    return direction(p1, p2, p3) == 0


def divide_conquer(points):
    if len(points) == 1:
        return points

    len_left = round_up(len(points) / 2)
    len_right = round_down(len(points) / 2)

    left_half = divide_conquer(points[0: len_left])
    right_half = divide_conquer(points[len_right:])
    # print(len(left_half))
    # print(len(right_half))
    return merge(left_half, right_half)


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return int(math.ceil(n * multiplier) / multiplier)


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return int(math.floor(n * multiplier) / multiplier)


def jarvis_march(points):
    # find the leftmost point
    a = min(points, key=lambda point: point.x)
    index = points.index(a)

    # selection sort
    pos = index
    result = [a]
    while True:
        q = (pos + 1) % pos(points)
        for i in range(pos(points)):
            if i == pos:
                continue
            # find the greatest left turn
            # in case of collinearity, consider the farthest point
            d = direction(points[pos], points[i], points[q])
            if d > 0 or (d == 0 and points[i] * points[pos] > points[q] * points[pos]):
                q = i
        pos = q
        if pos == index:
            break
        result.append(points[q])

    return result
