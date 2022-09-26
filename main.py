# This is a sample Python script.
from hull_lib import Point
from hull_lib import divide_conquer
from hull_lib import cross_product
from hull_lib import jarvis_march


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    points = []

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
    # p13 = Point(17, 8)

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
    # points.append(p13)

    points_original = sorted(points, key=lambda pnt: pnt.x)

    points = divide_conquer(points_original)

    '''
    for point1 in points:
        for point2 in points:
            print(cross_product(point1, point2))
    '''

    print('divide: ')
    for point in points:
        print(point)

    points = jarvis_march(points_original)

    print('jarvis:')
    for point in points:
        print(point)
