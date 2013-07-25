from numpy import arccos, array, cos, dot, pi, sin, sqrt

#############################################################################
#   CALCULATE THE AREA OF TRIANGLE A

def area(A):
    return (ED(A[0],A[1])*ED(A[1],(A[1][0],A[2][1])))/2.0

#############################################################################
#   FIND THE CENTROID OF TRIANGLE A

def centroid(A):
    return (A[0][0]+A[1][0]+A[2][0])/3.0,(A[0][1]+A[1][1]+A[2][1])/3.0

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO POINTS

def ED(a, b):
    return sqrt(((a[0]-b[0])**2)+((a[1]-b[1])**2))

#############################################################################
# TRANSLATE THE COORDINATES FOR TRIANGLE B SO THAT ITS CENTROID ALIGNS WITH
# THAT OF TRIANGLE A

def translate(A, B):
    A_c = centroid(A)
    B_c = centroid(B)
    x = A_c[0]-B_c[0]
    y = A_c[1]-B_c[1]
    return [(B[0][0]+x,B[0][1]+y),(B[1][0]+x,B[1][1]+y),(B[2][0]+x,B[2][1]+y)]

#############################################################################
# DETERMINE THE ROTATION OF TRIANGLE A IN RADIANS

def determine_rotation(A):
    A_c = centroid(A)
    a = ED(A_c,A[0])
    b = ED(A_c,(A_c[0],0))
    c = ED((A_c[0],0),A[0])
    angle = arccos(((a**2)+(b**2)-(c**2))/(2.0*a*b))
    if A[0][0] < A_c[0]:
        angle = pi+(pi-angle)
    return angle

#############################################################################
# ROTATE TRIANGLE A AROUND ITS CENTROID BY r RADIANS

def rot(A, r):
    pts = array([[A[0][0],A[0][1]],[A[1][0],A[1][1]],[A[2][0],A[2][1]]])
    A_c = centroid(A)
    cnt = array([A_c[0],A_c[1]])
    return dot(pts-cnt,array([[cos(r),sin(r)],[-sin(r),cos(r)]]))+cnt

#############################################################################
# ROTATE B SO THAT IT IS POINTING IN THE SAME DIRECTION AS A

def rotate(A, B):
    B = rot(B, determine_rotation(A)-determine_rotation(B))
    return [(B[0][0],B[0][1]),(B[1][0],B[1][1]),(B[2][0],B[2][1])]

#############################################################################
# SCALE TRIANGLE A SO THAT ITS AREA IS 100,000 SQUARE PIXELS

def scale(A):
    sf = sqrt(100000.0/area(A))
    A_c = centroid(A)
    return [((A[0][0]-A_c[0])*sf+A_c[0],(A[0][1]-A_c[1])*sf+A_c[1]),((A[1][0]-A_c[0])*sf+A_c[0],(A[1][1]-A_c[1])*sf+A_c[1]),((A[2][0]-A_c[0])*sf+A_c[0],(A[2][1]-A_c[1])*sf+A_c[1])]

#############################################################################
# TRANSLATE AND ROTATE B SO THAT IT IS LIKE A

def rigid_motion(A, B):
    return translate(A, rotate(A, B))

#############################################################################
# TRIANGLE DISTANCE MEASURES

def dT(A, B):
    return ED(A[0],B[0])+min(ED(A[1],B[1])+ED(A[2],B[2]),ED(A[1],B[2])+ED(A[2],B[1]))

def dT_up_to_translation(A, B):
    return dT(A, translate(A, B))

def dT_up_to_rotation(A, B):
    return dT(A, rotate(A, B))

def dT_up_to_scale(A, B):
    return dT(scale(A), scale(B))

def dT_up_to_rigid_motion(A, B):
    return dT(A, rigid_motion(A, B))

def dT_up_to_scaled_translation(A, B):
    return dT(scale(A), scale(translate(A, B)))

def dT_up_to_scaled_rotation(A, B):
    return dT(scale(A), scale(rotate(A, B)))

def dT_up_to_scaled_rigid_motion(A, B):
    return dT(scale(A), scale(rigid_motion(A, B)))
