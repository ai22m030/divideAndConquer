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
        self.count = 0

    def create(self, point):
        self.insert(point.x, point.y, 0)

    def add_head(self, point):
        self.create(point)

    def add_tail(self, point):
        self.insert(point.x, point.y, self.count)

    def delete(self, point):
        index = self.index(point)
        if index is not None:
            self.remove(index)

    def append(self, x, y):
        self.insert(x, y, self.count)
        return

    def insert(self, x, y, index):
        if (index > self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.head is None:
            self.head = Point(x, y)
            self.count = 1
            return

        temp = self.head
        if index == 0:
            temp = temp.ccw_next
        else:
            for _ in range(index - 1):
                temp = temp.cw_next

        temp.cw_next.ccw_next = Point(x, y)
        temp.cw_next.ccw_next.next, temp.cw_next.ccw_next.ccw_next = temp.cw_next, temp
        temp.cw_next = temp.cw_next.ccw_next
        if index == 0:
            self.head = self.head.ccw_next
        self.count += 1
        return

    def get(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        temp = self.head
        for _ in range(index):
            temp = temp.cw_next
        return temp

    def remove(self, index):
        if (index >= self.count) | (index < 0):
            raise ValueError(f"Index out of range: {index}, size: {self.count}")

        if self.count == 1:
            self.head = None
            self.count = 0
            return

        target = self.head
        for _ in range(index):
            target = target.cw_next

        if target is self.head:
            self.head = self.head.cw_next

        target.ccw_next.cw_next, target.cw_next.ccw_next = target.cw_next, target.ccw_next
        self.count -= 1

    def index(self, data):
        temp = self.head
        for i in range(self.count):
            if temp == data:
                return i
            temp = temp.cw_next
        return None

    def __iter__(self):
        point = self.head
        while point:
            yield point
            point = point.cw_next
            if point == self.head.cw_next:
                break


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cw_next = self
        self.ccw_next = self

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
        left_point = left_hull.get(left_hull.count - 1)
        right_point = right_hull.get(0)

        cp_left_point = left_point
        cp_right_point = right_point

        while True:
            prev_left_point = left_point
            prev_right_point = right_point
            if right_point.cw_next:
                # move p clockwise as long as it makes left turn
                while self.orientation(left_point, right_point, right_point.cw_next) == Orientation.LEFT:
                    del_right_point = right_point
                    right_point = right_point.cw_next
                    right_hull.delete(del_right_point)
            if left_point.ccw_next:
                # move p as long as it makes right turn
                while self.orientation(right_point, left_point, left_point.ccw_next) == Orientation.RIGHT:
                    del_left_point = left_point
                    left_point = left_point.ccw_next
                    left_hull.delete(del_left_point)

            if left_point == prev_left_point and right_point == prev_right_point:
                break

        # lower the bridge cp_p cp_q to the lower tangent
        while True:
            prev_left_point = cp_left_point
            prev_right_point = cp_right_point
            if cp_right_point.ccw_next:
                # move q as long as it makes right turn
                while self.orientation(cp_left_point, cp_right_point, cp_right_point.ccw_next) == Orientation.RIGHT:
                    del_right_point = cp_right_point
                    cp_right_point = cp_right_point.ccw_next
                    right_hull.delete(cp_right_point)
            if cp_left_point.cw_next:
                # move p as long as it makes left turn
                while self.orientation(cp_right_point, cp_left_point, cp_left_point.cw_next) == Orientation.LEFT:
                    del_left_point = cp_left_point
                    cp_left_point = cp_left_point.cw_next
                    left_hull.delete(del_left_point)
            if cp_left_point == prev_left_point and cp_right_point == prev_right_point:
                break

        hull = PointList()
        first = True

        for point in left_hull:
            if first:
                hull.create(Point(point.x, point.y))
            else:
                hull.add_tail(Point(point.x, point.y))

        for point in right_hull:
            if first:
                hull.create(Point(point.x, point.y))
            else:
                hull.add_tail(Point(point.x, point.y))

        return hull

    def brute_force(self, points):
        if len(points) == 3:
            p1 = Point(points[0, 0], points[0, 1])
            p2 = Point(points[1, 0], points[1, 1])
            p3 = Point(points[2, 0], points[2, 1])

            point_list = PointList()
            point_list.create(p1)

            ori = self.orientation(p1, p2, p3)

            if ori == Orientation.LEFT:
                point_list.add_head(p3)
                point_list.add_tail(p2)
            elif ori == Orientation.RIGHT:
                point_list.add_head(p2)
                point_list.add_tail(p3)

            if ori != Orientation.LINE:
                return point_list

            point_list.add_head(p3)
        elif len(points) == 2:
            p1 = Point(points[0, 0], points[0, 1])
            p2 = Point(points[1, 0], points[1, 1])

            point_list = PointList()
            point_list.create(p1)
            point_list.add_head(p2)
        else:
            p1 = Point(points[0, 0], points[0, 1])

            point_list = PointList()
            point_list.create(p1)

        return point_list
