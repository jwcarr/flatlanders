from scipy import sqrt, arccos

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

def ED(a, b):
    return sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

#############################################################################
#   CALCULATE THE HAUSDORFF DISTANCE BETWEEN TWO SHAPES

def HausdorffDistance(A, B):
    return max(max([min([ED(a,b) for b in B]) for a in A]), max([min([ED(a,b) for a in A]) for b in B]))

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO TRIANGLES

def triangleDistance(A, B):
    return ED(A[0],B[0])+min(ED(A[1],B[1])+ED(A[2],B[2]),ED(A[1],B[2])+ED(A[2],B[1]))

#############################################################################
#   CALCULATE THE DIFFERENCE IN AREA BETWEEN TWO TRIANGLES

def areaDistance(A, B):
    area_A = area(A[0], A[1], A[2])
    area_B = area(B[0], B[1], B[2])
    return abs(area_A-area_B)

#############################################################################
# TRANSLATE THE COORDINATES FOR TRIANGLE B SO THAT ITS CENTROID OR ORIENTING
# SPOT ALIGNS WITH THAT OF TRIANGLE A

def translate(A, B, alignment="centroid"):
    if alignment == "centroid":
        A_centroid = centroid(A[0], A[1], A[2])
        B_centroid = centroid(B[0], B[1], B[2])
        x_shift = A_centroid[0] - B_centroid[0]
        y_shift = A_centroid[1] - B_centroid[1]
    elif alignment == "spot":
        x_shift = A[0][0] - B[0][0]
        y_shift = A[0][1] - B[0][1]
    B1x = B[0][0] + x_shift
    B1y = B[0][1] + y_shift
    B2x = B[1][0] + x_shift
    B2y = B[1][1] + y_shift
    B3x = B[2][0] + x_shift
    B3y = B[2][1] + y_shift
    return [(B1x, B1y), (B2x, B2y), (B3x, B3y)]

def rotation(A):
    A_c = centroid(A[0], A[1], A[2])
    top_point = (A_c[0], 0)
    ori_spot = A[0]

    a = ED(A_c, ori_spot)
    b = ED(A_c, top_point)
    c = ED(top_point, ori_spot)

    return arccos(((a**2)+(b**2)-(c**2))/float(2*a*b))*(180.0/3.1415)
