import geometry
from numpy import array, log
from random import randrange
from scipy import std, mean
import matplotlib.pyplot as plt

def pointedness(T):
    perimeter = geometry.perimeter(T)
    area = geometry.area(T)
    expected_area = (perimeter**2)/20.784609691
    return log(expected_area / area)

def randomTriangle():
    x1 = randrange(0, 480)
    y1 = randrange(0, 480)
    x2 = randrange(0, 480)
    y2 = randrange(0, 480)
    x3 = randrange(0, 480)
    y3 = randrange(0, 480)
    return array([[x1,y1],[x2,y2],[x3,y3]])

def run(sims):
    scores = []
    for i in range(0,sims):
        p = pointedness(randomTriangle())
        if p < 10:
            scores.append(p)
    return scores
