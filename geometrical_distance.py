from itertools import combinations
from scipy.spatial.distance import squareform
import numpy as np
import basics
import geometry

########################################

def distance_matrix(triangles, distance_metric):
  n = len(triangles)
  distance_matrix = np.zeros([n, n], dtype=float)
  for i in range(0, n):
    for j in range(i+1, n):
      dist = distance_metric(triangles[i], triangles[j])
      distance_matrix[i, j] = dist
      distance_matrix[j, i] = dist
  return distance_matrix / distance_matrix.max()

def triangle_distance_matrix(triangles, distance_metrics):
  n = len(triangles)
  feature_matrices = []
  for feature in distance_metrics:
    feature_matrix = np.zeros([n, n], dtype=float)
    for metric in feature:
      feature_matrix += distance_matrix(triangles, metric)
    feature_matrices.append(feature_matrix / len(feature))
  return np.mean(feature_matrices, axis=0)

def combination_matrices(triangles, distance_metrics):
  n = len(distance_metrics)
  combins = []
  for i in range(1, n+1):
    for j in combinations(range(n), i):
      combins.append(j)
  combin_matrices = []
  for combin in combins:
    combin_metrics = []
    for i in combin:
      combin_metrics.append(distance_metrics[i])
    combin_matrices.append(triangle_distance_matrix(triangles, combin_metrics))
  return combin_matrices

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

# Given two rotations from North, return the shortest rotational distance

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

def most_and_least_similar_pairs(matrix):
  similar_score = 16
  dissimilar_score = 0
  n = matrix.shape[0]
  for i in range(0, n):
    for j in range(i+1, n):
      score = matrix[i, j]
      if score < similar_score:
        similar_score = score
        similar_indices = (i, j)
      if score > dissimilar_score:
        dissimilar_score = score
        dissimilar_indices = (i, j)
  return similar_score, similar_indices, dissimilar_score, dissimilar_indices

########################################

static_set_matrix = triangle_distance_matrix(1, 'A', 0, 's', metrics)
static_set_array = squareform(static_set_matrix, 'tovector')
def experiment_results(experiment):
  results = []
  for chain in basics.chain_codes[experiment-1]:
    results.append(chain_results(experiment, chain))
  return results

def chain_results(experiment, chain):
  results = []
  for generation in range(0,11):
    results.append(generation_results(experiment, chain, generation))
  return results

def generation_results(experiment, chain, generation):
  strings = basics.getWords(experiment, chain, generation, 's')
  if len(set(strings)) > 2:
    string_distances = basics.stringDistances(strings)
    best_r = -1
    for i in range(0, len(combin_matrices)):
      r = np.corrcoef(string_distances, squareform(combin_matrices[i]))[0,1]
      if r > best_r:
        best_matrix = i
        best_r = r
    return best_matrix + 1, best_r
  return None

########################################

metrics = [[boxOriC, boxOriE, boxVrtC, boxVrtE], [locOriX, locOriY, locCntX, locCntY], [rotOri, rotThin], [shpThin, shpWide, shpEqui], [sizArea, sizPeri, sizCent]]
