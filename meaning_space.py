#! /usr/bin/env python

import geometry
import numpy
from subprocess import call
import Mantel
import Levenshtein
from random import randrange

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]

def load(experiment, chain, generation, set_type):
  filename = "Data/" + str(experiment) + "/" + chain + "/" + str(generation) + set_type
  f = open(filename, 'r')
  data = f.read()
  f.close()
  rows = data.split("\n")
  matrix = []
  for row in rows:
    cells = row.split("\t")
    matrix.append(cells)
  return matrix

def getTriangles(experiment, chain, generation, set_type):
  if set_type == "c":
    data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
  else:
    data = load(experiment, chain, generation, set_type)
  triangles = []
  for row in data:
    x1, y1 = row[1].split(',')
    x2, y2 = row[2].split(',')
    x3, y3 = row[3].split(',')
    triangles.append(numpy.array([[float(x1),float(y1)],[float(x2),float(y2)],[float(x3),float(y3)]]))
  return triangles

def getWords(experiment, chain, generation, set_type):
  if set_type == "c":
    data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
  else:
    data = load(experiment, chain, generation, set_type)
  return [data[x][0] for x in range(0,len(data))]

def MakeFeatureMatrix(triangles, normalize=True):
  matrix = []
  for t in triangles:
    matrix.append(MakeFeatureVector(t))
  matrix = numpy.asarray(matrix, dtype=float)
  if normalize == True:
    for dim in range(0, matrix.shape[1]):
      minimum = matrix[:, dim].min()
      difference = matrix[:, dim].max() - minimum
      matrix[:, dim] = (matrix[:, dim] - minimum) / difference
  return matrix

def MakeFeatureVector(t):
  vector = []
  # Size features
  vector.append(geometry.area(t))             # 0  Area (exp dist)
  vector.append(geometry.perimeter(t))        # 1  Perimeter (norm dist)
  vector.append(geometry.centroid_size(t))    # 2  Centroid size (norm dist)

  # Location features
  vector.append(t[0][0])                      # 3  Location of orienting spot on x-axis (uni dist)
  vector.append(t[0][1])                      # 4  Location of orienting spot on y-axis (uni dist)
  vector.append(geometry.centroid(t)[0])      # 5  Location of centroid on x-axis (uni dist)
  vector.append(geometry.centroid(t)[1])      # 6  Location of centroid on y-axis (uni dist)

  # Rotation features
  vector.append(geometry.rotation(t))         # 7  Radial distance from north by orienting spot (uni dist)
  vector.append(geometry.rotation_by_smallest_angle(t)) # 8  Radial distance from north by smallest angle (uni dist)

  # Reflection features
  vector.append(abs(geometry.rotation(t)))    # 9  Absolute radial distance from north by orienting spot (uni dist)
  vector.append(abs(geometry.rotation_by_smallest_angle(t))) # 10 Absolute radial distance from north by smallest angle (uni dist)

  # Shape features
  vector.append(geometry.smallest_angle(t))   # 11 Angle of thinnest vertex (exp-ish, bit weird)
  vector.append(geometry.largest_angle(t))    # 12 Angle of widest vertex (exp-ish, bit weird)
  vector.append(geometry.std_angle(t))        # 13 Standard deviation of angles (sort of normal)

  # Bounding box features
  vector.append(geometry.dist_to_nearest_corner(t,0)) # 14 Distance from orienting spot to nearest corner (norm dist)
  vector.append(geometry.dist_to_nearest_edge(t,0)) # 15 Distance from orienting spot to nearest edge (exp dist)
  vector.append(numpy.mean([geometry.dist_to_nearest_corner(t,i) for i in range(0,3)])) # 16 Mean distance from vertices to nearest corner (norm dist)
  vector.append(numpy.mean([geometry.dist_to_nearest_edge(t,i) for i in range(0,3)])) # 17 Mean distance from vertices to nearest edge (norm dist)

  return numpy.asarray(vector, dtype=float)

# Read in a CSV file
def ReadCSV(filename):
  file_handle = open(filename)
  file_content = file_handle.read()
  file_handle.close()
  lines = file_content.split('\n')
  matrix = []
  for i in range(1, len(lines)-1):
    cells = lines[i].split(',')
    row = []
    for j in range(1, len(cells)):
      row.append(float(cells[j]))
    matrix.append(row)
  return matrix

# Write out a CSV file
def WriteCSV(matrix, filename):
  file_handle = open(filename, 'w')
  data = ''
  for row in matrix:
    data += ','.join(str(x) for x in row) + '\n'
  file_handle.write(data)
  file_handle.close()

# Calcualte the Euclidean distance in n-dimensional space
def ED(a, b):
  return numpy.sqrt(sum([(a[i]-b[i])**2 for i in range(0, len(a))]))

# Calcualte the Manhattan distance in n-dimensional space
def MD(a, b):
  return sum([abs(a[i]-b[i]) for i in range(0, len(a))])

# Scale pca scores (matrix) by their proportion of variance (array)
def scale(matrix, array):
  for i in range(len(matrix)):
    for j in range(len(matrix[0])):
      matrix[i][j] = matrix[i][j] * array[j][0]
  return matrix

# Get raw scores, run them through PCA to get PCA scores, scale by proportion of varience
def RunPCA(raw_scores, prop_var_scale=True):
  WriteCSV(raw_scores, 'pca_input.csv')
  call(["R", "CMD", "BATCH", "princomp.r"])
  pca_scores = ReadCSV('pca_output.csv')
  pca_prop_var = ReadCSV('pca_output_pv.csv')
  if prop_var_scale == True:
    pca_scores = scale(pca_scores, pca_prop_var)
  return pca_scores

# Take a feature matrix and convert to a distance matrix for each pair of objects
def DistanceMatrix(matrix, normalize=True):
  n = len(matrix)
  dist_matrix = []
  for i in range(0, n):
    for j in range(i+1, n):
      dist_matrix.append(ED(matrix[i], matrix[j]))
  if normalize == True:
    minimum = min(dist_matrix)
    difference = float(max(dist_matrix) - minimum)
    return [(dist_matrix[i] - minimum) / difference for i in range(len(dist_matrix))]
  return dist_matrix

# Take strings, calculate normalized Levenshtein edit distance, and return distance matrix
def stringDistances(strings):
  distances = []
  for i in range(0,len(strings)):
    for j in range(i+1,len(strings)):
      ld = Levenshtein.distance(strings[i], strings[j])
      distances.append(ld/float(max(len(strings[i]), len(strings[j]))))
  return distances

# For a given language, run everything and return the Mantel Test result
def run(experiment, chain, generation, set_type='s', randomizations=1000, normalize=True, run_pca=True, prop_var_scale=True):
  raw_scores = MakeFeatureMatrix(experiment, chain, generation, set_type, normalize)
  if run_pca == True:
    raw_scores = RunPCA(raw_scores, prop_var_scale)
  meaning_dists = DistanceMatrix(raw_scores)
  words = getWords(experiment, chain, generation, "s")
  string_dists = stringDistances(words)
  return Mantel.Test(meaning_dists, string_dists, randomizations)

def run_all(experiment, randomizations=1000, normalize=True, run_pca=True, prop_var_scale=True):
  matrix = []
  for chain in chain_codes[experiment-1]:
    row = []
    for gen in range(0, 11):
      row.append(run(experiment, chain, gen, 's', randomizations, normalize, run_pca, prop_var_scale)[5])
    matrix.append(row)
  return matrix

def randomTriangle():
    point1 = float(randrange(11, 491)), float(randrange(11, 491))
    point2 = float(randrange(11, 491)), float(randrange(11, 491))
    point3 = float(randrange(11, 491)), float(randrange(11, 491))
    return [point1, point2, point3]
