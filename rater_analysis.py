#! /usr/bin/env python

import matplotlib.pyplot as plt
from numpy import corrcoef, zeros
from copy import deepcopy
from scipy import spatial

########################################################################################

class Rater:

  def __init__(self, ID):
    self.ID = str(ID)
    self.matrix = self.ParseFile()
    self.orientation = self.matrix[0][1]
    self.ip_address = self.matrix[0][2]
    self.start_timestamp = int(self.matrix[0][3])
    self.end_timestamp = int(self.matrix[-2][3])
    self.time_taken = (self.end_timestamp - self.start_timestamp) / 60.0
    self.timecourse = [(int(self.matrix[i][3]) - self.start_timestamp) / 60.0 for i in range(0, 151)]
    self.comp_code = self.matrix[-1][0]
    del self.matrix[0]
    del self.matrix[-1]
    self.ratings, self.test_ratings, self.practice_ratings = self.SeparateMatrix()

  def ReadFile(self, filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content.split('\n')

  def ParseFile(self):
    file_content = self.ReadFile('Data/Ratings/' + self.ID)
    return [line.split('\t') for line in file_content]

  def SeparateMatrix(self):
    ratings = []
    test_ratings = []
    practice_ratings = []
    for row in self.matrix:
      # If rating is undefined, skip the row
      if row[2] != 'undefined':
        int_row = [int(row[0]), int(row[1]), int(row[2]), int(row[3])]
        if int_row[0] >= 0:
          ratings.append(int_row)
        else:
          if int_row[0] == int_row[1]:
            test_ratings.append(int_row)
          else:
            practice_ratings.append(int_row)
    return ratings, test_ratings, practice_ratings

  def GetRatings(self, kind):
    if kind == 'norm': target_matrix = self.ratings
    elif kind == 'prac': target_matrix = self.practice_ratings
    elif kind == 'test': target_matrix = self.test_ratings
    ratings = []
    for row in target_matrix:
      try:
        ratings.append(row[2])
      except ValueError:
        ratings.append(None)
    return ratings

  def GetNormRatings(self, kind):
    ratings = self.GetRatings(kind)
    minimum = min(ratings)
    difference = float(max(ratings) - minimum)
    return [(rating - minimum) / difference for rating in ratings]

  def NormMatrix(self, kind):
    if kind == 'norm': target_matrix = deepcopy(self.ratings)
    elif kind == 'prac': target_matrix = deepcopy(self.practice_ratings)
    elif kind == 'test': target_matrix = deepcopy(self.test_ratings)
    ratings = [row[2] for row in target_matrix]
    minimum = min(ratings)
    difference = float(max(ratings) - minimum)
    for row in target_matrix:
      row[2] = (row[2] - minimum) / difference
    return target_matrix

  def Hist(self, normalize=False, savefig=False):
    if normalize == True:
      ratings = self.GetNormRatings('norm')
      plt.hist(ratings, bins=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
      plt.xlim(0, 1)
    else:
      ratings = self.GetRatings('norm')
      plt.hist(ratings, bins=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
      plt.xlim(0, 1000)
    plt.ylim(0, 100)
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title('Rater ' + self.ID)
    if savefig == True:
      plt.savefig("hists/" + self.ID + ".pdf")
      plt.close()
    else:
      plt.show()

  def RaterReliability(self, distance_array):
    distance_matrix = spatial.distance.squareform(distance_array, 'tomatrix')
    x = []
    y = []
    for row in self.NormMatrix('norm'):
      x.append(distance_matrix[row[0], row[1]])
      y.append(row[2])
    return corrcoef(x, y)[0,1]

########################################################################################

def AverageDistanceMatrix(raters):
  count_matrix = zeros([48, 48], dtype=int)
  sum_distance_matrix = zeros([48, 48], dtype=float)
  for rater in raters:
    for row in rater.NormMatrix('norm'):
      sum_distance_matrix[row[0], row[1]] += float(row[2])
      sum_distance_matrix[row[1], row[0]] += float(row[2])
      count_matrix[row[0], row[1]] += 1
      count_matrix[row[1], row[0]] += 1
  sum_distance_array = spatial.distance.squareform(sum_distance_matrix, 'tovector')
  count_array = spatial.distance.squareform(count_matrix, 'tovector')
  mean_distance_array = sum_distance_array / count_array
  return mean_distance_array, count_array

########################################################################################

# Initialize a Rater object for each rater
raters = [Rater(i) for i in range(0, 96)]

# Average everyone's ratings together to form a (condensed) distance matrix
distance_array, count_array = AverageDistanceMatrix(raters)
