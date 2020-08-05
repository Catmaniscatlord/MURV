import numpy as np


def distance(point1, point2):
    #distance
    dist = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)
    return dist


#point1-point2
def subtractPoints(point1, point2):
    point = []

    if len(point1) == len(point2):
        for i in range(len(point1)):
            point.append(point1[i] - point2[i])
        return point
    else:
        print("points don't have the same length")
        return

#point1+point2
def addPoints(point1, point2):
    point = []
    if len(point1) == len(point2):
        for i in range(len(point1)):
            point.append(point1[i] + point2[i])
        return point
    else:
        print("points don't have the same length")
        return

# rotates a point around another by an angle
def rotatePoint(originPoint, rotatingPoint, xAngle, yAngle, zAngle):
    if originPoint == rotatingPoint:
        return originPoint
    relativePoint = np.array(subtractPoints(rotatingPoint, originPoint))
    rotationMatrix = np.array([
        [np.cos(zAngle) * np.cos(yAngle),
         np.cos(zAngle) * np.sin(yAngle) * np.sin(xAngle) - np.sin(zAngle) * np.cos(xAngle),
         np.cos(zAngle) * np.sin(yAngle) * np.cos(xAngle) + np.sin(zAngle) * np.sin(xAngle)],
        [np.sin(zAngle) * np.cos(yAngle),
         np.sin(zAngle) * np.sin(yAngle) * np.sin(xAngle) + np.cos(zAngle) * np.cos(xAngle),
         np.sin(zAngle) * np.sin(yAngle) * np.cos(xAngle) - np.cos(zAngle) * np.sin(xAngle)],
        [-np.sin(yAngle), np.cos(yAngle) * np.sin(xAngle), np.cos(yAngle) * np.cos(xAngle)]
    ])
    rotatedPoint = np.matmul(rotationMatrix, relativePoint)
    ajustedPoint = addPoints(rotatedPoint, originPoint)
    return ajustedPoint

# performs the same action as rotate point but does it for a set of points
def rotateGrid(originPoint, points, transform):
    for i in range(len(points)):
        points[i] = rotatePoint(originPoint, points[i], transform[0], transform[1], transform[2])
    return points

# translates grid by a set amount ie (1,1,1)+(3,2,5)=(4,3,6)
def translateGrid(points, transfrom):
    if len(points[0]) != len(transfrom):
        print("lengths are not equal")
    for i in range(len(points)):
        for j in range(len(points[i])):
            points[i][j] += transfrom[j]
    return points


# uses the location of each AP, along with its distance to the unknown point to locate the unknown point
def multiLateration(point1, point2, point3, distance1, distance2, distance3):
    points = [point1, point2, point3]
    r1, r2, r3 = distance1, distance2, distance3
    # transforms the grid into a more solveable state where all the AP's lie on the x-y plane
    transforms = [] #stores a list of all transforms so they can be undone later
    vector = subtractPoints(points[1], point1)
    points = rotateGrid(point1, points, [np.arctan(vector[1] / vector[2]), 0, 0])
    transforms.append([np.arctan(vector[1] / vector[2]), 0, 0])

    vector = subtractPoints(points[1], point1)
    points = rotateGrid(point1, points, [0, np.arctan(vector[2] / vector[0]), 0])
    transforms.append([0, np.arctan(vector[2] / vector[0]), 0])

    vector = subtractPoints(points[2], point1)
    points = rotateGrid(point1, points, [np.arctan(vector[1] / vector[2]) + np.pi / 2, 0, 0])
    transforms.append([np.arctan(vector[1] / vector[2]) + np.pi / 2, 0, 0])

    transforms.append(np.negative(point1))

    points=translateGrid(points, np.negative(point1))
    x = (points[1][0] ** 2 - r2 ** 2 + r1 ** 2) / (2 * points[1][0])
    a = (1 / (2 * points[1][0])) * np.sqrt(
        4 * (points[1][0] ** 2) * r2 ** 2 - (points[1][0] ** 2 - r1 ** 2 + r2 ** 2) ** 2)
    '''
    x=(x1^2-r2^2+r1^2)/(2*x1)
    a=(1/2x1)(sqrt(4*x1^2*r1^2-(x1^2-r2^2+r1^2)^2))
    '''
    y = ((((r3 ** 2 - r2 ** 2 - points[2][0] ** 2 + points[1][0] ** 2 - points[2][1] ** 2 + points[1][1] ** 2) / 2)
          - x * (-points[2][0] + points[1][0])) / (-points[2][1] + points[1][1]))
    '''
    y=(((r2^2-r1^2-x2^2+x1^2-y2^2+y1^2)/2)-x(-x2+x1))/(-y2+y1)
    '''
    z = np.sqrt(a ** 2 - y ** 2)
    # inserts the solved point into the array

    points.insert(3,[x,y,z])

    #transforms the array back to its original state
    points = translateGrid(points, np.negative(transforms[3]))
    points = rotateGrid(point1, points, np.negative(transforms[2]))
    points = rotateGrid(point1, points, np.negative(transforms[1]))
    points = rotateGrid(point1, points, np.negative(transforms[0]))


    return points
