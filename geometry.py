import scipy

#############################################################################
#   CALCULATE THE PERIMETER OF A TRIANGLE

def perimeter(a, b, c):
    return ED(a,b)+ED(b,c)+ED(a,c)

#############################################################################
#   CALCULATE THE AREA OF A TRIANGLE

def area(a, b, c):
    return (ED(a,b)*ED(b,(b[0],c[1])))/2.0

#############################################################################
#   FIND THE CENTROID OF A TRIANGLE

def centroid(a, b, c):
    return (a[0]+b[0]+c[0])/3.0, (a[1]+b[1]+c[1])/3.0

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO POINTS

def ED(point1, point2):
    return scipy.sqrt(((point1[0]-point2[0])**2)+((point1[1]-point2[1])**2))

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO TRIANGLES

def triangleDistance(A, B):
    return ED(A[0],B[0])+min(ED(A[1],B[1])+ED(A[2],B[2]),ED(A[1],B[2])+ED(A[2],B[1]))

#############################################################################
#   CALCULATE THE DIFFERENCE IN AREA BETWEEN TWO TRIANGLES

def areaDistance(A, B):
    area_A = area(A[0], A[1], A[2])
    area_B = area(B[0], B[1], B[2])
    return scipy.sqrt((area_A-area_B)**2)
