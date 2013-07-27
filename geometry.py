from numpy import arccos, array, cos, dot, sin, sqrt

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO POINTS

def ED(a, b):
    return sqrt(((a[0]-b[0])**2.0)+((a[1]-b[1])**2.0))

#############################################################################
#   CALCULATE THE AREA OF TRIANGLE A

def area(A):
    a, b, c = ED(A[0],A[1]), ED(A[1],A[2]), ED(A[2],A[0])
    s = (a+b+c)/2.0
    return sqrt(s*(s-a)*(s-b)*(s-c))

#############################################################################
#   FIND THE CENTROID OF TRIANGLE A

def centroid(A):
    return array([(A[0][0]+A[1][0]+A[2][0])/3.0,(A[0][1]+A[1][1]+A[2][1])/3.0])

#############################################################################
# TRANSLATE TRIANGLE B SO THAT ITS CENTROID ALIGNS WITH THAT OF TRIANGLE A

def translate(B, A):
    return B+(centroid(A)-centroid(B))

#############################################################################
# ROTATE TRIANGLE A SO THAT IT IS POINTING NORTH

def rotate(A):
    c = centroid(A)
    p, q, r = ED(c,A[0]), ED(c,(c[0],0)), ED((c[0],0),A[0])
    theta = arccos(((p**2.0)+(q**2.0)-(r**2.0))/(2.0*p*q))
    if A[0][0] > c[0]:
        theta = 0.0-theta
    return dot(A-c,array([[cos(theta),sin(theta)],[-sin(theta),cos(theta)]]))+c

#############################################################################
# SCALE TRIANGLE A SO THAT ITS AREA IS 18,00 SQUARE PIXELS

def scale(A):
    f = sqrt(18000.0/area(A))
    c = centroid(A)
    return ((A-c)*f)+c

#############################################################################
# TRIANGLE DISTANCE MEASURES

def dT(A, B):
    return ED(A[0],B[0])+min(ED(A[1],B[1])+ED(A[2],B[2]),ED(A[1],B[2])+ED(A[2],B[1]))

def dT_up_to_translation(A, B):
    return dT(A, translate(B, A))

def dT_up_to_rotation(A, B):
    return dT(rotate(A), rotate(B))

def dT_up_to_scale(A, B):
    return dT(scale(A), scale(B))

def dT_up_to_rigid_motion(A, B):
    return dT(rotate(A), translate(rotate(B), A))

def dT_up_to_scaled_translation(A, B):
    return dT(scale(A), scale(translate(B, A)))

def dT_up_to_scaled_rotation(A, B):
    return dT(scale(rotate(A)), scale(rotate(B)))

def dT_up_to_scaled_rigid_motion(A, B):
    return dT(scale(rotate(A)), scale(translate(rotate(B), A)))
