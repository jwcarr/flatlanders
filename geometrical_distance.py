from scipy.spatial.distance import squareform
import numpy as np
import basics
import geometry

########################################

def distance_matrix(triangles, distance_metric):
  n = len(triangles)
  distance_matrix = np.zeros([n, n], dtype=float)
  for i in range(0, len(triangles)):
    for j in range(i+1, len(triangles)):
      dist = distance_metric(triangles[i], triangles[j])
      distance_matrix[i, j] = dist
      distance_matrix[j, i] = dist
  return normalize(distance_matrix)

def normalize(distance_matrix):
  minimum = distance_matrix.min()
  delta = distance_matrix.max() - minimum
  return (distance_matrix - minimum) / delta

def composite_distance_matrix(triangles, distance_metrics):
  n = len(triangles)
  sum_distance_matrix = np.zeros([n, n], dtype=float)
  for distance_metric in distance_metrics:
    sum_distance_matrix += distance_matrix(triangles, distance_metric)
  return sum_distance_matrix

def triangle_distance_matrix(experiment, chain, generation, set_type, distance_metrics):
  triangles = basics.getTriangles(experiment, chain, generation, set_type)
  return composite_distance_matrix(triangles, distance_metrics)

########################################

# Distance metrics

def sizArea(t1, t2):
  return abs(geometry.area(t1) - geometry.area(t2))

def sizPeri(t1, t2):
  return abs(geometry.perimeter(t1) - geometry.perimeter(t2))

def sizCent(t1, t2):
  return abs(geometry.centroid_size(t1) - geometry.centroid_size(t2))

def locOriX(t1, t2):
  return abs(t1[0][0] - t2[0][0])

def locOriY(t1, t2):
  return abs(t1[0][1] - t2[0][1])

def locCntX(t1, t2):
  return abs(geometry.centroid(t1)[0] - geometry.centroid(t2)[0])

def locCntY(t1, t2):
  return abs(geometry.centroid(t1)[1] - geometry.centroid(t2)[1])

def rotOri(t1, t2):
  t1_rot = geometry.rotation(t1)
  t2_rot = geometry.rotation(t2)
  return smallest_rot(t1_rot, t2_rot)

def rotThin(t1, t2):
  t1_rot = geometry.rotation_by_smallest_angle(t1)
  t2_rot = geometry.rotation_by_smallest_angle(t2)
  return smallest_rot(t1_rot, t2_rot)

def shpThin(t1, t2):
  return abs(geometry.smallest_angle(t1) - geometry.smallest_angle(t2))

def shpWide(t1, t2):
  return abs(geometry.largest_angle(t1) - geometry.largest_angle(t2))

def shpEqui(t1, t2):
  return abs(geometry.equilateralness(t1) - geometry.equilateralness(t2))

def boxOriC(t1, t2):
  return abs(geometry.dist_to_nearest_corner(t1,0) - geometry.dist_to_nearest_corner(t2,0))

def boxOriE(t1, t2):
  return abs(geometry.dist_to_nearest_edge(t1,0) - geometry.dist_to_nearest_edge(t2,0))

def boxVrtC(t1, t2):
  dists1 = [geometry.dist_to_nearest_corner(t1,i) for i in range(0,3)]
  dists2 = [geometry.dist_to_nearest_corner(t2,i) for i in range(0,3)]
  return abs(np.mean(dists1) - np.mean(dists2))

def boxVrtE(t1, t2):
  dists1 = [geometry.dist_to_nearest_edge(t1,i) for i in range(0,3)]
  dists2 = [geometry.dist_to_nearest_edge(t2,i) for i in range(0,3)]
  return abs(np.mean(dists1) - np.mean(dists2))

########################################

# Given two rotations from Noth, return the shortest rotational distance

def smallest_rot(t1_rot, t2_rot):
  # If both rotations have the same sign...
  if t1_rot * t2_rot > 0:
    # ... just return the absolute difference
    return abs(t1_rot - t2_rot)
  else:
    # Sum the rotations
    theta = abs(t1_rot) + abs(t2_rot)
    # If the sum of rotations is greater than pi
    if theta > np.pi:
      # ... subtract the sum from 2pi
      return (2 * np.pi) - theta
    return theta

########################################

metrics = [sizArea, sizPeri, sizCent, locOriX, locOriY, locCntX, locCntY, rotOri, rotThin, shpThin, shpWide, shpEqui, boxOriC, boxOriE, boxVrtC, boxVrtE]
static_set_matrix = triangle_distance_matrix(1, 'A', 0, 's', metrics)
static_set_array = squareform(static_set_matrix, 'tovector')
