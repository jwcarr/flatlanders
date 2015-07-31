import matplotlib.pyplot as plt
from numpy import corrcoef, mean, zeros
from copy import deepcopy
from scipy import spatial

########################################################################################

class Rater:

  def __init__(self, ID):
    self.ID = str(ID)
    self.matrix = self.ReadFile()
    self.orientation = self.matrix[0][1]
    self.ip_address = self.matrix[0][2]
    self.start_timestamp = int(self.matrix[0][3])
    self.end_timestamp = int(self.matrix[-2][3])
    self.time_taken = (self.end_timestamp - self.start_timestamp) / 60.0
    self.timecourse = [(int(self.matrix[i][3]) - self.start_timestamp) / 60.0 for i in range(0, 151)]
    self.completion_code = self.matrix[-1][0]
    del self.matrix[0]
    del self.matrix[-1]
    self.ratings, self.test_ratings, self.practice_ratings = self.SeparateMatrix()
    self.normalized_ratings = self.MakeNormalizedMatrix()

  # Read in a ratings file
  def ReadFile(self):
    try:
      f = open('Data/ratings/' + self.ID)
    except IOError:
      raise ValueError(self.ID + ' is not a valid rater')
    content = f.read()
    f.close()
    return [line.split('\t') for line in content.split('\n')]

  # Separate out the raw data into three matrices: actual ratings, practice ratings, and test ratings
  def SeparateMatrix(self):
    ratings = []
    test_ratings = []
    practice_ratings = []
    for i in range(0, len(self.matrix)):
      if self.matrix[i][2] == 'undefined':
        continue # If rating is undefined, skip the row
      int_row = [int(self.matrix[i][0]), int(self.matrix[i][1]), int(self.matrix[i][2]), int(self.matrix[i][3])]
      if int_row[0] == int_row[1]:
        test_ratings.append(int_row)
      elif i < 6:
        practice_ratings.append(int_row)
      else:
        ratings.append(int_row)
    return ratings, test_ratings, practice_ratings

  # Normalize actual ratings over the interval [0,1]
  def MakeNormalizedMatrix(self):
    normalized_ratings = deepcopy(self.ratings)
    ratings = self.GetRatings('actual')
    try:
      minimum = min(ratings)
    except ValueError:
      print self.ID, ratings
    difference = float(max(ratings) - minimum)
    if difference == 0.0:
      return False
    for row in normalized_ratings:
      row[2] = (row[2] - minimum) / difference
    return normalized_ratings

  # Extract ratings of a given kind
  def GetRatings(self, kind):
    if kind == 'actual': target_matrix = self.ratings
    elif kind == 'practice': target_matrix = self.practice_ratings
    elif kind == 'test': target_matrix = self.test_ratings
    elif kind == 'normalized': target_matrix = self.normalized_ratings
    else:
      return False
    ratings = []
    for row in target_matrix:
      try:
        ratings.append(row[2])
      except ValueError:
        continue
    return ratings

  # Produce a histogram of the actual ratings (raw or normalized)
  def Hist(self, normalize=False, savefig=False):
    if normalize == True:
      ratings = self.GetRatings('normalized')
      plt.hist(ratings, bins=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
      plt.xlim(0, 1)
    else:
      ratings = self.GetRatings('actual')
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

  # Measure rater agreement by correlating this rater's ratings with the mean ratings of all raters
  def RaterAgreement(self, distances=False):
    x = []
    y = []
    if type(distances) == bool and distances == False:
      distances = all_distance_array
    distance_matrix = spatial.distance.squareform(distances, 'tomatrix')
    for row in self.normalized_ratings:
      x.append(distance_matrix[row[0], row[1]])
      y.append(row[2])
    return corrcoef(x, y)[0,1]

  def MeanTestRating(self):
    return mean(self.GetRatings('test'))

########################################################################################

# Average together the normalized ratings of many raters
def AverageDistanceMatrix(raters, agreement_filter=None, distances=None):
  count_matrix = zeros([48, 48], dtype=int)
  sum_distance_matrix = zeros([48, 48], dtype=float)
  for rater in raters:
    normalized_matrix = rater.normalized_ratings
    if normalized_matrix == False:
      continue # If the normalized matrix doesn't exist, skip the rater. This can occur if
               # the rater gives the same rating for every pair of triangles.
    if agreement_filter != None and rater.RaterAgreement(distances) < agreement_filter:
      continue # If filter is being applied and the rater is not good enough, skip the rater
    for row in normalized_matrix:
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
all_distance_array, all_count_array = AverageDistanceMatrix(raters, None, None)

# Average everyone's ratings together again, this time filtering out unreliable raters.
# Reliable raters are defined as those whose agreement with the average ratings of all
# raters is greater than 0.4.
reliable_distance_array, reliable_count_array = AverageDistanceMatrix(raters, 0.4, all_distance_array)
