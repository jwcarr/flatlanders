from itertools import combinations
from scipy.spatial.distance import squareform
from scipy.stats import rankdata
import numpy as np
import basics
import geometry

########################################

# Generate a rank distance matrix for a given geometrical metric

def feature_matrix(triangles, distance_metric):
  n = len(triangles)
  # Store the distance between each pair of triangles
  distance_array = []
  for i in range(0, n):
    for j in range(i+1, n):
      distance_array.append(distance_metric(triangles[i], triangles[j]))
  # Convert to ranks to remove distributional effects of each metric
  return rankdata(distance_array)

# Generate a set of feature matrices given a set of geometrical metrics

def feature_matrices(triangles, distance_metrics):
  matrices = []
  # For each distance metric (i.e. each feature)...
  for metric in distance_metrics:
    # Compute and store the distance matrix
    matrices.append(feature_matrix(triangles, metric))
  return matrices

# Enumerate all combinations of matrices and sum them together

def combination_matrices(matrices):
  n = len(matrices) # Number of features
  combin_matrices = []
  # For i = 1 ... n
  for i in range(1, n+1):
    # For each combination in "n choose i"...
    for combination_indices in combinations(range(n), i):
      # Sum the relevant matrices together for a composite distance matrix
      sum_matrix = np.sum([matrices[j] for j in combination_indices], axis=0)
      # Normalize and store the composite matrix
      combin_matrices.append(sum_matrix / sum_matrix.max())
  # Return all the combination matrices
  return combin_matrices

########################################

# Euclidean distance between centroids

def location_distance(t1, t2):
  return geometry.ED(geometry.centroid(t1), geometry.centroid(t2))

# Shortest radial distance by orienting spot

def orientation_distance(t1, t2):
  t1_rot = geometry.rotation(t1)
  t2_rot = geometry.rotation(t2)
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

# Absolute distance between cetroid sizes

def size_distance(t1, t2):
  return abs(geometry.centroid_size(t1) - geometry.centroid_size(t2))

# Absolute difference between equilateralness ratios

def shape_distance(t1, t2):
  return abs(geometry.equilateralness(t1) - geometry.equilateralness(t2))

########################################

# Given a sparse distance matrix, return the most similar and most dissimilar pairs

def most_and_least_similar_pairs(distance_array):
  distance_matrix = squareform(distance_array, force='tomatrix')
  similar_score = 1
  dissimilar_score = 0
  n = distance_matrix.shape[0]
  for i in range(0, n):
    for j in range(i+1, n):
      score = distance_matrix[i, j]
      if score < similar_score:
        similar_score = score
        similar_indices = (i, j)
      if score > dissimilar_score:
        dissimilar_score = score
        dissimilar_indices = (i, j)
  return similar_score, similar_indices, dissimilar_score, dissimilar_indices

# Count the number of occurrences of each type
# Pass in a list of results from experiment_results()

def type_counts(results):
  types = [0 for i in range(15)]
  for experiment in results:
    for chain in experiment:
      for i in range(1, len(chain)):
        try:
          types[chain[i][0]-1] += 1
        except TypeError:
          continue
  return types

# Format results into a LaTeX table

def latex_table(results, experiment):
  latex = ''
  for chain in range(0, len(results)):
    chain_line = []
    chain_line.append( '\\bfseries %s' % basics.chain_codes[experiment-1][chain] )
    for generation in range(1,11):
      try:
        if results[chain][generation][1] >= 0:
          corr = "{0:.2f}".format(results[chain][generation][1])[1:]
        else:
          corr = '-' + "{0:.2f}".format(results[chain][generation][1])[2:]
        if corr[-1] == '0':
          corr = corr[:-1]
        cell = str(results[chain][generation][0]) + ' (' + corr  + ')'
      except TypeError:
        cell = '--'
      chain_line.append(cell)
    latex += ' & '.join(chain_line)
    latex += '\\\\\n'
  latex = ('\multicolumn{11}{c}{\\bfseries Experiment %i} \\\\ \\hline\n'% experiment) + latex[0:-1] + ' \hline'
  f = open(basics.desktop_location + 'E%i_typology.tex'%experiment, 'w')
  f.write(latex)
  f.close()

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
      r = np.corrcoef(string_distances, all_combination_matrices[i])[0,1]
      if r > best_r:
        best_matrix = i
        best_r = r
    # Return type number and correlation coefficient for combination of features with strongest correlation
    return best_matrix + 1, best_r
  return None

########################################

metrics = [location_distance, orientation_distance, shape_distance, size_distance]
static_set_triangles = basics.getTriangles(1, 'A', 0, 's')
individual_matrices = feature_matrices(static_set_triangles, metrics)
all_combination_matrices = combination_matrices(individual_matrices)
