from itertools import combinations
from scipy.spatial.distance import squareform
import numpy as np
import basics
import geometry

########################################

# Generate a normalized distance matrix for a given geometrical metric

def property_distance_matrix(triangles, distance_metric):
  n = len(triangles) # Number of triangles
  # Create an empty distance matrix...
  distance_matrix = np.zeros([n, n], dtype=float)
  # ... and fill it in using the given metric
  for i in range(0, n):
    for j in range(i+1, n):
      dist = distance_metric(triangles[i], triangles[j])
      distance_matrix[i, j] = dist
      distance_matrix[j, i] = dist
  # Normalize simply by dividing by max value, since distance matrices will always have a min of 0
  return distance_matrix / distance_matrix.max()

# Generate a composite distance matrix by combining properties into feature matrices
# and averaging the feature matrices together

def composite_distance_matrix(triangles, distance_metrics):
  n = len(triangles) # Number of triangles
  feature_matrices = []
  # For each feature...
  for feature in distance_metrics:
    # create an empty feature distance matrix
    feature_matrix = np.zeros([n, n], dtype=float)
    # For each metric within that feature...
    for metric in feature:
      # add on the property distance matrix
      feature_matrix += property_distance_matrix(triangles, metric)
    # Divide by the number of metrics to get the mean and store in feature_matrices
    feature_matrices.append(feature_matrix / len(feature))
  # Averge the feature matrices together for a composite distance matrix
  return np.mean(feature_matrices, axis=0)

# Enumerate all combinations of given features and create a composite distance
# matrix for each combination

def combination_matrices(triangles, distance_metrics):
  n = len(distance_metrics) # Number of features
  combin_matrices = []
  # For i = 1 ... n
  for i in range(1, n+1):
    # For each combination in "n choose i"...
    for combination_indices in combinations(range(n), i):
      # Create a list of metrics to use
      combin_metrics = [distance_metrics[j] for j in combination_indices]
      # Create the composite distance matrix for that combination of metrics and store it
      combin_matrices.append(composite_distance_matrix(triangles, combin_metrics))
  # Return all the combination matrices
  return combin_matrices

########################################

# Geometrical distance metrics: Each returns the absolute difference between two triangles

# SIZE: Area
def sizArea(t1, t2):
  return abs(geometry.area(t1) - geometry.area(t2))

# Size: Perimeter
def sizPeri(t1, t2):
  return abs(geometry.perimeter(t1) - geometry.perimeter(t2))

# SIZE: Centroid size
def sizCent(t1, t2):
  return abs(geometry.centroid_size(t1) - geometry.centroid_size(t2))

# LOCATION: Orienting spot on x-axis
def locOriX(t1, t2):
  return abs(t1[0][0] - t2[0][0])

# LOCATION: Orienting spot on y-axis
def locOriY(t1, t2):
  return abs(t1[0][1] - t2[0][1])

# LOCATION: Centroid on x-axis
def locCntX(t1, t2):
  return abs(geometry.centroid(t1)[0] - geometry.centroid(t2)[0])

# LOCATION: Centroid on y-axis
def locCntY(t1, t2):
  return abs(geometry.centroid(t1)[1] - geometry.centroid(t2)[1])

# ROTATION: Based on orienting spot
def rotOri(t1, t2):
  t1_rot = geometry.rotation(t1)
  t2_rot = geometry.rotation(t2)
  return smallest_rot(t1_rot, t2_rot)

# ROTATION: Based on thinnest vertex
def rotThin(t1, t2):
  t1_rot = geometry.rotation_by_smallest_angle(t1)
  t2_rot = geometry.rotation_by_smallest_angle(t2)
  return smallest_rot(t1_rot, t2_rot)

# SHAPE: Angle of thinnest vertex
def shpThin(t1, t2):
  return abs(geometry.smallest_angle(t1) - geometry.smallest_angle(t2))

# SHAPE: Angle of widest vertex
def shpWide(t1, t2):
  return abs(geometry.largest_angle(t1) - geometry.largest_angle(t2))

# SHAPE: Equilateralness ratio
def shpEqui(t1, t2):
  return abs(geometry.equilateralness(t1) - geometry.equilateralness(t2))

# BOUNDING BOX RELATIONSHIP: Distance from orienting spot to nearest corner
def boxOriC(t1, t2):
  return abs(geometry.dist_to_nearest_corner(t1,0) - geometry.dist_to_nearest_corner(t2,0))

# BOUNDING BOX RELATIONSHIP: Distance from orienting spot to nearest edge
def boxOriE(t1, t2):
  return abs(geometry.dist_to_nearest_edge(t1,0) - geometry.dist_to_nearest_edge(t2,0))

# BOUNDING BOX RELATIONSHIP: Mean distance from vertices to nearest corner
def boxVrtC(t1, t2):
  dists1 = [geometry.dist_to_nearest_corner(t1,i) for i in range(0,3)]
  dists2 = [geometry.dist_to_nearest_corner(t2,i) for i in range(0,3)]
  return abs(np.mean(dists1) - np.mean(dists2))

# BOUNDING BOX RELATIONSHIP: Mean distance from vertices to nearest edge
def boxVrtE(t1, t2):
  dists1 = [geometry.dist_to_nearest_edge(t1,i) for i in range(0,3)]
  dists2 = [geometry.dist_to_nearest_edge(t2,i) for i in range(0,3)]
  return abs(np.mean(dists1) - np.mean(dists2))

########################################

# Given two rotations from North, return the shortest rotational distance.
# Required for rotOri() and rotThin()

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

# Given a sparse distance matrix, return the most similar and most dissimilar pairs

def most_and_least_similar_pairs(matrix):
  similar_score = 1
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

# Functions for generating experiment, chain, or generation results

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
  # Return None if there are < 3 unique strings
  if len(set(strings)) > 2:
    string_distances = basics.stringDistances(strings)
    # Iterate through feature combinations to find the best correlation
    best_r = -1
    for i in range(0, len(all_combination_matrices)):
      r = np.corrcoef(string_distances, squareform(all_combination_matrices[i]))[0,1]
      if r > best_r:
        best_matrix = i
        best_r = r
    # Return type number and correlation coefficient for combination of features with strongest correlation
    return best_matrix + 1, best_r
  return None

########################################

metrics_by_feature = [[boxOriC, boxOriE, boxVrtC, boxVrtE], [locOriX, locOriY, locCntX, locCntY], [rotOri, rotThin], [shpThin, shpWide, shpEqui], [sizArea, sizPeri, sizCent]]
static_set_triangles = basics.getTriangles(1, 'A', 0, 's')
all_combination_matrices = combination_matrices(static_set_triangles, metrics_by_feature)
