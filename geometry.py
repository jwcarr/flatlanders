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

def areaOfTriangle(x1, y1, x2, y2, x3, y3):
    base = distanceBetweenPoints(x1, y1, x2, y2)
    height = distanceBetweenPoints(x2, y2, x3, y3)
    square_area = base * height
    triangle_area = square_area / 2.0
    return triangle_area

#############################################################################
#   CALCULATE THE DISTANCE BETWEEN TWO COORDINATES

def distanceBetweenPoints(x1, y1, x2, y2):
    return scipy.sqrt(((x1 - x2)**2)+((y1 - y2)**2))
