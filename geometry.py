import scipy

#############################################################################
#   CALCULATE AVERAGE LINE LENGTH

def averageLineLength(x1, y1, x2, y2, x3, y3):
    AB = distanceBetweenPoints(x1, y1, x2, y2)
    BC = distanceBetweenPoints(x2, y2, x3, y3)
    AC = distanceBetweenPoints(x1, y1, x3, y3)
    return (AB + BC + AC) / 3.0

#############################################################################
#   CALCULATE THE AREA OF A TRIANGLE

def area(x1, y1, x2, y2, x3, y3):
    base = distanceBetweenPoints(x1, y1, x2, y2)
    height = distanceBetweenPoints(x2, y2, x2, y3)
    return (base * height) / 2.0

#############################################################################
#   FIND THE CENTROID OF A TRIANGLE

def centroid(x1, y1, x2, y2, x3, y3):
    return (x1+x2+x3)/3.0, (y1+y2+y3)/3.0

#############################################################################
#   CALCULATE THE ANGLES OF A TRIANGLE

def angles(x1, y1, x2, y2, x3, y3):
    AB = distanceBetweenPoints(x1, y1, x2, y2)
    BC = distanceBetweenPoints(x2, y2, x3, y3)
    AC = distanceBetweenPoints(x1, y1, x3, y3)
    h = max(AB, BC, AC)
    return 

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO POINTS

def distanceBetweenPoints(x1, y1, x2, y2):
    return scipy.sqrt(((x1 - x2)**2)+((y1 - y2)**2))