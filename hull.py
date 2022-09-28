# Convex hull calculations
from enum import Enum
import matplotlib


class Orientation(Enum):
    LEFT = 1
    RIGHT = 2
    LINE = 3


class PointList:
    def __init__(self):
        self.head = None
        self.tail = None

    def create(self, point):
        point.cw_next = None
        point.ccw_next = None
        self.head = point
        self.tail = point

    def add_head(self, point):
        self.head.ccw_next = point
        point.cw_next = self.head
        self.head = point
        self.tail.cw_next = self.head
        self.head.ccw_next = self.tail

    def add_tail(self, point):
        if self.head is None:
            self.head = point
            self.tail = point
            return

        last_point = self.head

        while last_point.cw_next != self.head:
            last_point = last_point.cw_next

        last_point.cw_next = point
        point.ccw_next = last_point

        self.tail = point
        self.tail.cw_next = self.head
        self.head.ccw_next = self.tail

    def delete(self, point):
        if self.head is None:
            return

        tmp_point = self.head
        found = False

        while tmp_point:
            if tmp_point == point:
                found = True
                break
            tmp_point = tmp_point.next

        if found:
            prev_point = tmp_point.ccw_next
            next_point = tmp_point.cw_next
            prev_point.cw_next = next_point
            next_point.ccw_next = prev_point
            return
        else:
            print("Element not found.")

    @staticmethod
    def add_middle(prev_point, x, y):
        if prev_point is None:
            print("Mentioned node doesn't exist")
            return

        next_point = prev_point.cw_next
        new_point = Point(x, y)
        prev_point.cw_next = new_point
        new_point.ccw_next = prev_point
        new_point.cw_next = next_point
        next_point.ccw_next = new_point

    def __iter__(self):
        point = self.head
        while point:
            yield point
            point = point.cw_next
            if point == self.tail.cw_next:
                break


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw_next = None
        self.ccw_next = None

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')\nCW:' \
                '(' + str(self.cw_next.x) + ', ' + str(self.cw_next.y) + ')\nCCW:' \
                '(' + str(self.ccw_next.x) + ', ' + str(self.ccw_next.y) + ')'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __mul__(self, p):
        return self.x * p.y - p.x * self.y

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)


class ConvexHull:
    def __init__(self, points, visual=False):
        if visual:
            matplotlib.use('TkAgg')

        self.visual = visual
        self.raw_points = points

    def orientation(self, p_line_1, p_line_2, p_check):
        orient = ((p_line_1.x - p_check.x) * (p_line_2.y - p_check.y)) - \
                 ((p_line_1.y - p_check.y) * (p_line_2.x - p_check.x))

        if orient > 0:
            return Orientation.LEFT
        elif orient < 0:
            return Orientation.RIGHT
        else:
            return Orientation.LINE

    def divide_conquer(self):
        return self.divide(self.raw_points[self.raw_points[:, 0].argsort()])

    def divide(self, points):
        if len(points) <= 3:
            return self.brute_force(points)

        return self.conquer(self.divide(points[0:int(len(points) / 2), :]),
                            self.divide(points[int(len(points) / 2):, :]))

    def conquer(self, left_hull, right_hull):
        left_point = left_hull[-1]
        right_point = right_hull[0]

        cp_p = left_point
        cp_q = right_point

        while True:
            prev_p = left_point
            prev_q = right_point
            if right_point.cw_next:
                # move p clockwise as long as it makes left turn
                while self.orientation(left_point, right_point, right_point.cw_next) == Orientation.LEFT:
                    right_point = right_point.cw_next
            if left_point.ccw_next:
                # move p as long as it makes right turn
                while self.orientation(right_point, left_point, left_point.ccw_next) == Orientation.RIGHT:
                    left_point = left_point.ccw_next

            if left_point == prev_p and right_point == prev_q:
                break

        # lower the bridge cp_p cp_q to the lower tangent
        while True:
            prev_p = cp_p
            prev_q = cp_q
            if cp_q.ccw_next:
                # move q as long as it makes right turn
                while self.orientation(cp_p, cp_q, cp_q.ccw_next) == Orientation.RIGHT:
                    cp_q = cp_q.ccw_next
            if cp_p.cw_next:
                # move p as long as it makes left turn
                while self.orientation(cp_q, cp_p, cp_p.cw_next) == Orientation.LEFT:
                    cp_p = cp_p.cw_next
            if cp_p == prev_p and cp_q == prev_q:
                break

        # remove all other points
        left_point.cw_next = right_point
        right_point.ccw_next = left_point

        cp_p.ccw_next = cp_q
        cp_q.cw_next = cp_p

        # final result
        result = []
        start = left_point
        while True:
            result.append(left_point)
            left_point = left_point.ccw_next

            if left_point == start:
                break

        return result

    def brute_force(self, points):
        if len(points) == 3:
            p1 = Point(points[0, 0], points[0, 1])
            p2 = Point(points[1, 0], points[1, 1])
            p3 = Point(points[2, 0], points[2, 1])



            ori = self.orientation(p1, p2, p3)

            if ori == Orientation.LEFT:
                p1.cw_next = p3
                p1.ccw_next = p2
            elif ori == Orientation.RIGHT:
                p1.cw_next = p2
                p1.ccw_next = p3

            if ori != Orientation.LINE:
                p1.cw_next.cw_next = p1.ccw_next
                p1.cw_next.ccw_next = p1
                p1.ccw_next.cw_next = p1
                p1.ccw_next.ccw_next = p1.cw_next

            if ori == Orientation.LEFT:
                return [p1, p1.ccw_next, p1.cw_next]
            elif ori == Orientation.RIGHT:
                return [p1, p1.cw_next, p1.ccw_next]

            p1.cw_next = p3
            p1.ccw_next = p1.cw_next
        elif len(points) == 2:
            p1 = Point(points[0, 0], points[0, 1])
            p2 = Point(points[1, 0], points[1, 1])

            p1.cw_next = p2
            p1.ccw_next = p1.cw_next
        else:
            p1 = Point(points[0, 0], points[0, 1])

            p1.cw_next = p1
            p1.ccw_next = p1.cw_next

        p1.cw_next.ccw_next = p1
        p1.cw_next.cw_next = p1
        p1.ccw_next.ccw_next = p1
        p1.ccw_next.cw_next = p1

        return [p1, p1.cw_next]
