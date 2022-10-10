# Convex hull calculations
from enum import Enum
import matplotlib
import copy


class Orientation(Enum):
    LEFT = 1
    RIGHT = 2
    LINE = 3


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __mul__(self, p):
        return self.x * p.y - p.x * self.y

    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)


class PointList:
    def __init__(self):
        self.data = []

    def add_head(self, point):
        self.data.reverse()
        self.data.append(point)
        self.data.reverse()

    def add_tail(self, point):
        self.data.append(point)

    def head(self):
        if len(self.data) > 0:
            return self.data[0]

        return None

    def tail(self):
        if len(self.data) > 0:
            return self.data[len(self.data) - 1]

        return None

    def delete(self, point):
        if point in self.data:
            self.data.remove(point)

    def clock_wise(self, point):
        if point in self.data:
            index = self.data.index(point)
            if index == 0:
                index = len(self.data) - 1
            else:
                index = index - 1

            return self.data[index]

        return None

    def counter_clock_wise(self, point):
        if point in self.data:
            index = self.data.index(point)
            if index == len(self.data) - 1:
                index = 0
            else:
                index = index + 1

            return self.data[index]

        return None

    def index(self, point):
        if point in self.data:
            return self.data.index(point)

        return None

    def size(self):
        return len(self.data)

    def __iter__(self):
        for i in range(len(self.data) - 1):
            yield self.data[i]


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

    def lower_tangent(self, p1, p2, points):
        for p in points:
            if p != p1 and p != p2 and self.orientation(p1, p2, p) == Orientation.LEFT:
                return False

        return True

    def upper_tangent(self, p1, p2, points):
        for p in points:
            if p != p1 and p != p2 and self.orientation(p1, p2, p) == Orientation.RIGHT:
                return False

        return True

    def divide_conquer(self):
        return self.divide(self.raw_points[self.raw_points[:, 0].argsort()])

    def divide(self, points):
        if len(points) <= 3:
            return self.brute_force(points)

        return self.conquer(self.divide(points[0:int(len(points) / 2), :]),
                            self.divide(points[int(len(points) / 2):, :]))

    def brute_force(self, points):
        if len(points) == 3:
            p1 = Point(points[0, 0], points[0, 1])
            p2 = Point(points[1, 0], points[1, 1])
            p3 = Point(points[2, 0], points[2, 1])

            point_list = PointList()
            point_list.add_head(p1)

            ori = self.orientation(p1, p2, p3)

            if ori == Orientation.LEFT:
                point_list.add_head(p3)
                point_list.add_tail(p2)
            elif ori == Orientation.RIGHT:
                point_list.add_head(p2)
                point_list.add_tail(p3)

            if ori != Orientation.LINE:
                return point_list

            point_list.add_tail(p3)
        elif len(points) == 2:
            p1 = Point(points[0, 0], points[0, 1])
            p2 = Point(points[1, 0], points[1, 1])

            point_list = PointList()
            point_list.add_head(p1)
            point_list.add_tail(p2)
        else:
            p1 = Point(points[0, 0], points[0, 1])

            point_list = PointList()
            point_list.add_head(p1)

        return point_list

    def conquer(self, left_hull, right_hull):
        cp_left_hull = copy.deepcopy(left_hull)
        cp_right_hull = copy.deepcopy(right_hull)

        left_hull_point = left_hull.tail()
        right_hull_point = right_hull.head()

        while not self.lower_tangent(left_hull_point, right_hull_point, cp_left_hull) or not self.lower_tangent(left_hull_point, right_hull_point, cp_left_hull):
            while not self.lower_tangent(left_hull_point, right_hull_point, cp_left_hull):
                del_point = left_hull_point
                left_hull_point = left_hull.clock_wise(left_hull_point)
                cp_left_hull.delete(del_point)
            while not self.lower_tangent(left_hull_point, right_hull_point, cp_right_hull):
                del_point = right_hull_point
                right_hull_point = right_hull.counter_clock_wise(right_hull_point)
                cp_right_hull.delete(del_point)

        left_hull_point = left_hull.tail()
        right_hull_point = right_hull.head()

        while not self.upper_tangent(right_hull_point, left_hull_point, cp_left_hull) or not self.upper_tangent(right_hull_point, left_hull_point, cp_right_hull):
            while not self.upper_tangent(right_hull_point, left_hull_point, cp_left_hull):
                del_point = left_hull_point
                left_hull_point = left_hull.counter_clock_wise(left_hull_point)
                cp_left_hull.delete(del_point)
            while not self.upper_tangent(right_hull_point, left_hull_point, cp_right_hull):
                del_point = right_hull_point
                right_hull_point = right_hull.clock_wise(right_hull_point)
                cp_right_hull.delete(del_point)

        hull = PointList()

        print(cp_left_hull.data)
        print(cp_right_hull.data)

        for point in cp_left_hull:
            hull.add_tail(point)

        for point in cp_right_hull:
            hull.add_tail(point)

        return hull
