

from operator import itemgetter


#
#
def main():


    point1 = (1, 2)
    point2 = (3, 6)
    point3 = (5, 4)
    point4 = (-1, 3)


    points = list()

    points.append(point1)
    points.append(point2)
    points.append(point3)
    points.append(point4)

    print()
    print('Raw data: --------------------------')

    print(points)

    for p in points:

        print()
        print(p)
        print(f'first = {p[0]}, second = {p[1]}')

        x, y = p
        print(f'x = {x}, y = {y}')



    # find maxes and mins
    maxx = max(points, key=itemgetter(0))
    minx = min(points, key=itemgetter(0))

    maxy = max(points, key=itemgetter(1))
    miny = min(points, key=itemgetter(1))

    print()
    print('Maxima/Minima: ---------------------')
    print(f'max x pair: {maxx}')
    print(f'max x: {maxx[0]}')
    print(f'min x pair: {minx}')
    print(f'min x: {minx[0]}')

    print(f'max y pair: {maxy}')
    print(f'max y: {maxy[1]}')
    print(f'min y pair: {miny}')
    print(f'min y: {miny[1]}')

    # sorts


    sorted_x = sorted(points, key=itemgetter(0))
    sorted_y = sorted(points, key=itemgetter(1))

    print()
    print('Sort: -----------------------')
    print(f'sorted on x: {sorted_x}')
    print(f'sorted on y: {sorted_y}')






if __name__ == '__main__':
    main()

