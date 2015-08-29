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
# TRANSLATE TRIANGLE B SO THAT ITS CENTROID ALIGNS WITH THAT OF TRIANGLE A

def translate(B, A):
  return B+(centroid(A)-centroid(B))

#############################################################################
# ROTATE TRIANGLE A SO THAT IT IS POINTING NORTH

def rotate(A):
  c = centroid(A)
  if A[0][0] == c[0]:
    if A[0][1] > c[1]:
      theta = np.pi
    else:
      return A
  else:
    p, q, r = ED(c,A[0]), ED(c,(c[0],0)), ED((c[0],0),A[0])
    theta = np.arccos(((p**2.0)+(q**2.0)-(r**2.0))/(2.0*p*q))
    if A[0][0] > c[0]:
      theta = 0.0-theta
  return np.dot(A-c,np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]]))+c

#############################################################################
# SCALE TRIANGLE A SO THAT ITS PERIMETER IS 750 PIXELS

def scale(A):
  f = 750.0/perimeter(A)
  c = centroid(A)
  return ((A-c)*f)+c

#############################################################################
# RETURN THE SMALLEST ANGLE IN RADIANS

def smallest_angle(A):
  smallest_ang = 10.0
  for vertex in range(1, 4):
    ang = angle(A, vertex)
    if ang < smallest_ang:
      smallest_ang = ang
  return smallest_ang

#############################################################################
# RETURN THE LARGEST ANGLE IN RADIANS

def largest_angle(A):
  largest_ang = 0.0
  for vertex in range(1, 4):
    ang = angle(A, vertex)
    if ang > largest_ang:
      largest_ang = ang
  return largest_ang

#############################################################################
# RETURN THE MEAN ANGLE IN RADIANS

def mean_angle(A):
  angles = []
  for vertex in range(1, 4):
    angles.append(angle(A, vertex))
  return np.mean(angles)

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
# RETURN THE RADIAL DISTANCE FROM NORTH FOR TRIANGLE A BY SMALLEST ANGLE

def rotation_by_smallest_angle(A):
  a, b, c = angle(A,1), angle(A,2), angle(A,3)
  angles = {'a':a, 'b':b, 'c':c}
  min_ang = min(angles, key=angles.get)
  if min_ang == 'a':
    A = np.array([[A[0][0], A[0][1]], [A[1][0], A[1][1]], [A[2][0], A[2][1]]])
  elif min_ang == 'b':
    A = np.array([[A[1][0], A[1][1]], [A[2][0], A[2][1]], [A[0][0], A[0][1]]])
  elif min_ang == 'c':
    A = np.array([[A[2][0], A[2][1]], [A[0][0], A[0][1]], [A[1][0], A[1][1]]])
  return rotation(A)

#############################################################################
# DISTANCE FROM A GIVEN VERTEX TO THE NEAREST CORNER OR EDGE

def dist_to_nearest_corner(A, vertex):
  corners = [(0,0), (0,500), (500,0), (500,500)]
  smallest_dist = 99999999.9
  for corner in corners:
    dist = ED(A[vertex], corner)
    if dist < smallest_dist:
      smallest_dist = dist
  return smallest_dist

def dist_to_nearest_edge(A, vertex):
  edges = [(A[vertex][0], 0), (0, A[vertex][1]), (A[vertex][0], 500), (500, A[vertex][1])]
  smallest_dist = 99999999.9
  for edge in edges:
    dist = ED(A[vertex], edge)
    if dist < smallest_dist:
      smallest_dist = dist
  return smallest_dist

#############################################################################
# EQUILATERALNESS RATIO

def upper_bound_on_area(p):
  return p**2.0 / 20.784609690826528

def equilateralness(A):
  a = area(A)
  p = perimeter(A)
  return a / upper_bound_on_area(p)

#############################################################################
# Return Bookstain coordinates for triangle A

def Bookstein_coordinates(A):
  BC_x = ((A[1,0]-A[0,0])*(A[2,0]-A[0,0])+(A[1,1]-A[0,1])*(A[2,1]-A[0,1])) / (((A[1,0]-A[0,0])**2) + ((A[1,1]-A[0,1])**2))
  BC_y = ((A[1,0]-A[0,0])*(A[2,1]-A[0,1])-(A[1,1]-A[0,1])*(A[2,0]-A[0,0])) / (((A[1,0]-A[0,0])**2) + ((A[1,1]-A[0,1])**2))
  return np.array([BC_x, BC_y])