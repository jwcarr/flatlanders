import numpy as np

#############################################################################
#   CALCULATE THE EUCLIDEAN DISTANCE BETWEEN TWO POINTS

def ED(a, b):
  return np.sqrt(((a[0]-b[0])**2.0)+((a[1]-b[1])**2.0))

#############################################################################
#   CALCULATE THE ANGLE OF A VERTEX

def angle(A, vertex):
  if vertex == 1:
    p, q, r = ED(A[2],A[0]), ED(A[0],A[1]), ED(A[1],A[2])
  elif vertex == 2:
    p, q, r = ED(A[0],A[1]), ED(A[1],A[2]), ED(A[2],A[0])
  elif vertex == 3:
    p, q, r = ED(A[1],A[2]), ED(A[2],A[0]), ED(A[0],A[1])
  return np.arccos(((p**2.0)+(q**2.0)-(r**2.0))/(2.0*p*q))

#############################################################################
#   CALCULATE THE AREA OF TRIANGLE A

def area(A):
  a, b, c = ED(A[0],A[1]), ED(A[1],A[2]), ED(A[2],A[0])
  s = (a+b+c)/2.0
  return np.sqrt(s*(s-a)*(s-b)*(s-c))

#############################################################################
#   CALCULATE THE PERIMETER OF TRIANGLE A

def perimeter(A):
  return ED(A[0],A[1])+ED(A[1],A[2])+ED(A[2],A[0])

#############################################################################
#   CALCULATE THE CENTROID SIZE OF TRIANGLE A

def centroid_size(A):
  c = centroid(A)
  centroid_size = 0.0
  for vertex in A:
    centroid_size += ED(vertex, c)**2
  return np.sqrt(centroid_size)

#############################################################################
#   FIND THE CENTROID OF TRIANGLE A

def centroid(A):
  return np.array([(A[0][0]+A[1][0]+A[2][0])/3.0,(A[0][1]+A[1][1]+A[2][1])/3.0])

#############################################################################
# ROTATE TRIANGLE A SO THAT IT IS POINTING NORTH

def rotate(A):
  theta = rotation(A)
  c = centroid(A)
  return np.dot(A-c,np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]]))+c

#############################################################################
# RETURN THE RADIAL DISTANCE FROM NORTH FOR TRIANGLE A BY ORIENTING SPOT

def rotation(A):
  c = centroid(A)
  if A[0][0] == c[0]:
    if A[0][1] > c[1]:
      theta = np.pi
    else:
      theta = 0.0
  else:
    p, q, r = ED(c,A[0]), ED(c,(c[0],0)), ED((c[0],0),A[0])
    theta = np.arccos(((p**2.0)+(q**2.0)-(r**2.0))/(2.0*p*q))
    if A[0][0] > c[0]:
      theta = 0.0-theta
  return theta

#############################################################################
# EQUILATERALNESS RATIO

def upper_bound_on_area(p):
  return p**2.0 / 20.784609690826528

def equilateralness(A):
  a = area(A)
  p = perimeter(A)
  return a / upper_bound_on_area(p)
