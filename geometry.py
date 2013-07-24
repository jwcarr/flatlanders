from scipy import arccos, array, cos, dot, pi, sin, sqrt

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
#   CALCULATE THE DIFFERENCE IN AREA BETWEEN TWO TRIANGLES

def areaDistance(A, B):
    area_A = area(A[0], A[1], A[2])
    area_B = area(B[0], B[1], B[2])
    return abs(area_A-area_B)

#############################################################################
# TRANSLATE THE COORDINATES FOR TRIANGLE B SO THAT ITS CENTROID OR ORIENTING
# SPOT ALIGNS WITH THAT OF TRIANGLE A

def translate(A, B):
    A_centroid = centroid(A[0], A[1], A[2])
    B_centroid = centroid(B[0], B[1], B[2])
    x_shift = A_centroid[0] - B_centroid[0]
    y_shift = A_centroid[1] - B_centroid[1]
    B1x = B[0][0] + x_shift
    B1y = B[0][1] + y_shift
    B2x = B[1][0] + x_shift
    B2y = B[1][1] + y_shift
    B3x = B[2][0] + x_shift
    B3y = B[2][1] + y_shift
    return [(B1x, B1y), (B2x, B2y), (B3x, B3y)]

#############################################################################
# DETERMINE THE ROTATION OF TRIANGLE A IN RADIANS

def rotation(A):
    '''Determine the rotation of triangle A'''
    A_c = centroid(A[0], A[1], A[2])
    top_point = (A_c[0], 0)
    a = ED(A_c, A[0])
    b = ED(A_c, top_point)
    c = ED(top_point, A[0])
    ang = arccos(((a**2)+(b**2)-(c**2))/float(2*a*b))
    if A[0][0] < A_c[0]:
        ang = pi + (pi-ang)
    return ang

#############################################################################
# ROTATE TRIANGLE A AROUND ITS CENTROID BY ang RADIANS

def rotate(A, ang):
    '''Rotate triangle A around its centroid by ang radians'''
    pts = array([[A[0][0], A[0][1]], [A[1][0], A[1][1]], [A[2][0], A[2][1]]])
    c = centroid(A[0], A[1], A[2])
    cnt = array([c[0], c[1]])
    return dot(pts-cnt,array([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt

#############################################################################
# ROTATE B SO THAT IT IS POINTING IN THE SAME DIRECTION AS A

def align_rotations(A, B):
    '''Rotate B so that it is pointing in the same direction as A'''
    A_rotation = rotation(A)
    B_rotation = rotation(B)
    B_r = rotate(B, A_rotation-B_rotation)
    B = [(B_r[0][0], B_r[0][1]), (B_r[1][0], B_r[1][1]), (B_r[2][0], B_r[2][1])]
    return B

#############################################################################
# SCALE TRIANGLE A SO THAT ITS AREA IS 100,000 SQUARE PIXELS

def scale(A):
    ar = area(A[0], A[1], A[2])
    sf = sqrt(100000.0/float(ar))
    A_c = centroid(A[0], A[1], A[2])
    A = [((A[0][0]-A_c[0])*sf+A_c[0], (A[0][1]-A_c[1])*sf+A_c[1]),
         ((A[1][0]-A_c[0])*sf+A_c[0], (A[1][1]-A_c[1])*sf+A_c[1]),
         ((A[2][0]-A_c[0])*sf+A_c[0], (A[2][1]-A_c[1])*sf+A_c[1])]
    return A

#############################################################################
# TRANSLATE AND ROTATE B SO THAT IT IS LIKE A

def rigid_motion(A, B):
    return translate(A, align_rotations(A, B))

#############################################################################
# TRIANGLE DISTANCE MEASURES

def dT(A, B):
    return ED(A[0],B[0])+min(ED(A[1],B[1])+ED(A[2],B[2]),ED(A[1],B[2])+ED(A[2],B[1]))

def dT_up_to_translation(A, B):
    return dT(A, translate(A, B))

def dT_up_to_rotation(A, B):
    return dT(A, align_rotations(A, B))

def dT_up_to_scale(A, B):
    return dT(scale(A), scale(B))

def dT_up_to_rigid_motion(A, B):
    return dT(A, rigid_motion(A, B))

def dT_up_to_scaled_translation(A, B):
    return dT(scale(A), scale(translate(A, B)))

def dT_up_to_scaled_rotation(A, B):
    return dT(scale(A), scale(align_rotations(A, B)))

def dT_up_to_isometry(A, B):
    return dT(scale(A), scale(rigid_motion(A, B)))
