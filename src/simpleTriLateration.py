import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import multiLateration as ml
def main():
    #initializes the points
    x0, y0, z0 = 4, 1, 10  # point we are trying to find

    x1, y1, z1 = 3, 2, 3    #AP1
    x2, y2, z2 = -1, -3, 5  #AP2
    x3, y3, z3 = 1, 4, -2   #AP3
    p0 = [x0, y0, z0]
    p1 = [x1, y1, z1]
    p2 = [x2, y2, z2]
    p3 = [x3, y3, z3]
    points = [p0, p1, p2, p3]
    print(points)

    #distance between AP's and unknown point
    r1=ml.distance(points[0],points[1])
    r2=ml.distance(points[0],points[2])
    r3=ml.distance(points[0],points[3])


    points=ml.multiLateration(points[1],points[2],points[3],r1,r2,r3)

    # Plots the points into a 3d graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points[0][0], points[0][1], points[0][2], label="unkown point", c="black")
    ax.scatter(points[1][0], points[1][1], points[1][2], label="AP 1", c="red")
    ax.scatter(points[2][0], points[2][1], points[2][2], label="AP 2", c="red")
    ax.scatter(points[3][0], points[3][1], points[3][2], label="AP 3", c="red")
    ax.legend()
    plt.show()


main()