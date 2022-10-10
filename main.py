# This is a sample Python script.
from hull_lib import Point
from hull_lib import divide_conquer
from hull_lib import orientation
from hull_lib import Orientation
import matplotlib
import numpy as np
from hullv2 import ConvexHull
# from scipy.spatial import ConvexHull, convex_hull_plot_2d
from matplotlib import pyplot as plt

from hull_lib import jarvis_march


if __name__ == '__main__':
    matplotlib.use('TkAgg')
    rng = np.random.default_rng()
    points = rng.random((12, 2))
    # points = points[points[:, 0].argsort()]
    # points = np.sort(points, axis=0)
    # print(points)
    # print(points[:, 0])
    # print(points[:, 1])
    for p in points:
        plt.plot(p[0], p[1], marker="o", markeredgecolor="black", markerfacecolor="black")

    hull = ConvexHull(points)
    points_result = hull.divide_conquer()

    print(points_result.data)

    first = True
    print_hull = np.array([[points_result.head().x, points_result.head().y]])
    for p in points_result:
        if first:
            first = False
        else:
            print_hull = np.append(print_hull, [[p.x, p.y]], axis=0)
    print_hull = np.append(print_hull, [[points_result.head().x, points_result.head().y]], axis=0)

    print(print_hull)

    plt.plot(print_hull[:, 0], print_hull[:, 1], '-ok', markeredgecolor="black", markerfacecolor="black")
    plt.show()
    '''
    p1 = Point(2, 2)
    p2 = Point(3, 4)
    p3 = Point(7, 3)
    p4 = Point(5, 2)
    p5 = Point(7, 5)
    p6 = Point(5, 6)
    p7 = Point(11, 5)
    p8 = Point(15, 7)
    p9 = Point(12, 3)
    p10 = Point(15, 3)
    p11 = Point(16, 5)
    p12 = Point(12, 7)
    p13 = Point(17, 8)
    '''

    '''
    p1.cw_next = p2
    p1.ccw_next = p4
    p2.cw_next = p6
    p2.ccw_next = p1
    p3.cw_next = p4
    p3.ccw_next = p5
    p4.cw_next = p1
    p4.ccw_next = p3
    p5.cw_next = p3
    p5.ccw_next = p6
    p6.cw_next = p5
    p6.ccw_next = p2
    p7.cw_next = p12
    p7.ccw_next = p9
    p8.cw_next = p11
    p8.ccw_next = p12
    p9.cw_next = p7
    p9.ccw_next = p10
    p10.cw_next = p9
    p10.ccw_next = p11
    p11.cw_next = p10
    p11.ccw_next = p8
    p12.cw_next = p8
    p12.ccw_next = p7
    '''
    # p13.ccw_next = p12
    # p13.cw_next = p7

    '''
    points.append(p1)
    points.append(p2)
    points.append(p3)
    points.append(p4)
    points.append(p5)
    points.append(p6)
    points.append(p7)
    points.append(p8)
    points.append(p9)
    points.append(p10)
    points.append(p11)
    points.append(p12)
    points.append(p13)
    '''

    # plt.rcParams["figure.figsize"] = [20.00, 10]
    # plt.rcParams["figure.autolayout"] = True
    # p1 = Point(2, 2)
    # p2 = Point(3, 4)
    # p3 = Point(7, 3)
    # p4 = Point(8, 2)
    # p5 = Point(10, 5)
    # p6 = Point(8, 6)
    # x = [2, 3, 7, 2]
    # y = [2, 4, 3, 2]
    # x1 = [8, 10, 8, 8]
    # y1 = [2, 5, 6, 2]
    # plt.xlim(0, 5)
    # plt.ylim(0, 5)
    # plt.grid()
    # plt.plot(x, y, '-ok', marker="o", markeredgecolor="black", markerfacecolor="black")
    # plt.plot(x1, y1, '-ok', marker="o", markeredgecolor="black", markerfacecolor="black")
    '''
    for p in points:
        plt.plot(p.x, p.y, '-ok', marker="o", markeredgecolor="black", markerfacecolor="black")
    '''
    # plt.show()

    # rng = np.random.default_rng()
    # points = rng.random((30, 2))  # 30 random points in 2-D
    # print(points)
    # hull = ConvexHull(points)
    # print(hull.simplices)

    # plt.plot(points[:, 0], points[:, 1], 'o')

    # for simplex in hull.simplices:
    #    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

    # plt.show()

    # points_original = sorted(points, key=lambda pnt: pnt.x)

    # points = divide_conquer(points_original)

    '''
    for point1 in points:
        for point2 in points:
            print(point1 * point2)
    '''

    # print(Point(2, 5) * Point(2, 4))

    # print('divide: ')
    # for point in points:
    #     print(point)
    '''
    points = jarvis_march(points_original)

    print('jarvis:')
    for point in points:
        print(point)
    '''
