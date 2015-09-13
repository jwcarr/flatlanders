from collections import defaultdict
import matplotlib.pyplot as plt
from numpy import corrcoef, mean
from copy import deepcopy
import basics
import Krippendorff

########################################################################################

class Rater:

  def __init__(self, ID):
    self.ID = ID
    self.matrix = self.ReadFile()
    self.orientation = self.matrix[0][1]
    self.ip_address = self.matrix[0][2]
    self.start_timestamp = int(self.matrix[0][3])
    self.end_timestamp = int(self.matrix[-2][3])
    self.time_taken = (self.end_timestamp - self.start_timestamp) / 60.0
    self.timecourse = [(int(self.matrix[i][3]) - self.start_timestamp) / 60.0 for i in range(0, len(self.matrix)-1)]
    self.completion_code = self.matrix[-1][0]
    del self.matrix[0]
    del self.matrix[-1]
    self.comments = self.ReadInComments()
    self.ratings, self.test_ratings, self.practice_ratings = self.SeparateMatrix()
    self.normalized_ratings = self.MakeNormalizedMatrix()

  # Read in a ratings file
  def ReadFile(self):
    try:
      f = open('../data/task_2/' + self.ID)
    except IOError:
      raise ValueError(self.ID + ' is not a valid rater')
    content = f.read()
    f.close()
    return [line.split('\t') for line in content.split('\n')]

  # Read in a comments file
  def ReadInComments(self):
    try:
      f = open('../data/task_2/comments/' + self.ID)
    except IOError:
      return None
    comment = f.read()
    f.close()
    return comment.replace('\r\n', ' ').replace('\n', ' ')

  # Separate out the raw data into three matrices: actual ratings, practice ratings, and test ratings
  def SeparateMatrix(self):
    ratings = []
    test_ratings = []
    practice_ratings = []
    for i in range(0, len(self.matrix)):
      form_row = [self.matrix[i][0], self.matrix[i][1], int(self.matrix[i][2]), int(self.matrix[i][3])]
      if form_row[0] == form_row[1]:
        test_ratings.append(form_row)
      elif i < 6:
        practice_ratings.append(form_row)
      else:
        ratings.append(form_row)
    return ratings, test_ratings, practice_ratings

  # Normalize actual ratings over the interval [0,1]
  def MakeNormalizedMatrix(self):
    normalized_ratings = deepcopy(self.ratings)
    ratings = self.GetRatings('actual')
    minimum = min(ratings)
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
    return [row[2] for row in target_matrix]

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
  def RaterAgreement(self, distances=None):
    if self.normalized_ratings == False:
      return None
    if distances == None:
      distances = all_distances
    x = []
    y = []
    for row in self.normalized_ratings:
      x.append(distances[row[0] + '~' + row[1]])
      y.append(row[2])
    return corrcoef(x, y)[0,1]

  def MeanTestRating(self):
    return mean(self.GetRatings('test'))

########################################################################################

# Average together the normalized ratings of many raters
def AverageRatings(agreement_filter=None, test_filter=None, distances=None, krippendorff=False):
  sum_dist = defaultdict(float)
  mean_dist = defaultdict(float)
  counts = defaultdict(float)
  ka_data = {}
  ka_ignore = []
  rater_n = 0
  rater_i = -1
  for rater in raters.keys():
    rater_i += 1
    if raters[rater].normalized_ratings == False:
      #print('Excluding rater %s because the ratings cannot be normalized' % raters[rater].ID)
      ka_ignore.append(rater_i)
      continue # If the normalized matrix doesn't exist, skip the rater. This can occur if
               # the rater gives the same rating for every pair of triangles.
    if agreement_filter != None:
      rater_agreement = raters[rater].RaterAgreement(distances)
      if rater_agreement < agreement_filter:
        #print('Excluding rater %s due to low rater agreement: %f' % (raters[rater].ID, rater_agreement))
        ka_ignore.append(rater_i)
        continue # If filter is being applied and the rater is not good enough, skip the rater
    if test_filter != None:
      mean_test_rating = raters[rater].MeanTestRating()
      if mean_test_rating > test_filter:
        #print('Excluding rater %s due to a high average test rating: %f' % (raters[rater].ID, mean_test_rating))
        ka_ignore.append(rater_i)
        continue # If test filter is being applied and the rater is not good enough, skip the rater
    rater_n += 1
    for row in raters[rater].normalized_ratings:
      pair = row[0] + '~' + row[1]
      sum_dist[pair] += row[2]
      counts[pair] += 1.0
      if krippendorff == True:
        try:
          ka_data[pair][rater_i] = row[2]
        except KeyError:
          ka_data[pair] = [None]*len(raters.keys())
          ka_data[pair][rater_i] = row[2]
  for pair in sum_dist.keys():
    mean_dist[pair] = sum_dist[pair] / counts[pair]
  if krippendorff == True:
    ka_matrix = [[None]*len(ka_data.keys()) for i in range(len(raters.keys()))]
    pair_i = 0
    for pair in ka_data.keys():
      for rater_i in range(len(raters.keys())):
        ka_matrix[rater_i][pair_i] = ka_data[pair][rater_i]
      pair_i += 1
    for ignore_i in reversed(sorted(ka_ignore)):
      del ka_matrix[ignore_i]
    return mean_dist, counts, rater_n, ka_matrix
  return mean_dist, counts, rater_n, None

#############################################################################

# Measure communicative error
def CommError(chain, generation, distances=None):
  if distances == None:
    distances = reliable_distances
  dynamic_set = basics.load(3, chain, generation, "d")
  static_set = basics.load(3, chain, generation, "s")
  triangle_pairs = []
  for item in dynamic_set+static_set:
    target_triangle = item[1] + ';' + item[2] + ';' + item[3]
    selected_triangle = item[5] + ';' + item[6] + ';' + item[7]
    if target_triangle != selected_triangle:
      triangle_pairs.append(target_triangle + '~' + selected_triangle)
  error = 0.0
  for pair in triangle_pairs:
    error += distances[pair]
  return error

# Measure communicative accuracy for all chains and generations
def error_results(distances=None):
  results = [[CommError(chain, gen, distances) for gen in range(1,11)] for chain in ['I', 'J', 'K', 'L']]
  dataset = {'data':results, 'experiment':3, 'starting_generation':1, 'data_type':'communicative_error'}
  return dataset

#############################################################################

# Measure communicative accuracy - number of correct trials
def CommAccuracy(chain, generation):
  dynamic_set = basics.load(3, chain, generation, "d")
  static_set = basics.load(3, chain, generation, "s")
  accuracy = 0
  for item in dynamic_set+static_set:
    target_triangle = item[1] + ';' + item[2] + ';' + item[3]
    selected_triangle = item[5] + ';' + item[6] + ';' + item[7]
    if target_triangle == selected_triangle:
      accuracy += 1
  return accuracy

# Measure communicative accuracy for all chains and generations
def accuracy_results():
  results = [[CommAccuracy(chain, gen) for gen in range(1,11)] for chain in ['I', 'J', 'K', 'L']]
  dataset = {'data':results, 'experiment':3, 'starting_generation':1, 'data_type':'communicative_accuracy'}
  return dataset

########################################################################################

rater_ids = ['RMta7V', 'OkC5LB', '6qLDuu', 'GHenhK', 'foMrWq', 'epHboY', 'bskf5M', 'NKSxRE', 'aXemPV', 'cVaABH', 'Ce4mEV', 'UBEEJA', '0PW6xm', 'tHDQaA', 'EnDYyj', 'U3zEci', 'jIIGEq', 'LbhJA2', 'eQP8Fm', 'SodXwQ', 'iWsaSj', '7LBzg2', 'frx7RY', 'RsEzuJ', '3ZyRRQ', 'cXAjeA', 'ZAihTJ', 'zfRLjU', 'cStvq7', 'hsFArm', 'tk0W7z', 'NQY9bH', 'P1riul', 'UhIFMT', 'AtRWfx', '5yeIpA', 'u6zH8w', 'rltdaN', 'mqsczS', 'PLB9jo', '03n4Ps', 'e5eCFn', 'Xa0q7w', 'x69VP4', 'HIdxeo', 'KUEtYW', '9D3B3k', 'lekIGt', 'EOT6sn', 'T1raSK', 'e0rZ1Y', 'twLkTs', '7tEgXa', 'C1k7uB', 'qpoRlE', 'GnYZ2D', 'OS1YmD', 'hlsn85', 'jkN91v', 'gkgIxF', 'tQWwcZ', 'NdMcUG', 'iRlbmk', '5Pnkze', 'adWJUA', 'lPi5if', 'AQpNFI', 'NMeQyt', 'rwDh1S', 'sbJbvJ', 'zGovuZ', 'B6NxzU', 'blmZFW', 'FHxs7m', 'K7SpWm', 'qoC9Iq', 'a7Ouyu', 'umI9vl', 'fEICAJ', 'n7ESGD', 'mqjvzr', 'N0D9Dj', 'J1Ev8v', 'zms547', '4p0l19', 'dAkLBc', 'qKvAD6', 'j6euM6', 'krwnGt', 'TOs2fl', 'p78HV9', 'w9W551', '4035mM', '1MiLH7', 'YPHNwF', 'LZSGOC', 'fBfJk5', 'xsBBiP', 'InoQiR', '3Z9qcH', 'FXFtPV', '7KLEnT', '7BEQRV', 'YTBdAV', 'sx1DHV', 'J2jvhY', 'U5NmXx', '5Dm1B0', '3g4sob', 'zhBLCn', 'ocN3sS', '7wwEFS', 'g1lqlK', 'WBbYCs', 'DiDOZd', 'R3DMso', '5CqAjK', 'YgkDcT', 'Oq4clq', 'bE170R', 'UGIp7F', 'OydqKh', 'fuFez9', 'jsJmSI', 'MRWJIw', 'Igmw1w', 'kviCDe', 'sKW5iW', 'lRKFkQ', 'pqJ71a', '0UWPAh', 'ieo3JV', 'jAdzzP', 'jErsKs', 'FcVU5v', 'PDKIV3', 'HNIGDC', 'euXIPq', 'Zm4M8U', 'iybJZk', 'BRX5W8', 'ai6GyL', 'svubHN', 'IMiD1n', 'RkECnA', 'XKJ88u', 'tPPoxT', '1vrqxm', 'EBXy1C', 'OMMo1f', '8f7Vtq', 'SsoWcI', 'k3QKem', '2rTLol', '8fOexH', 'JhcpFr', 'SwD4VX', 'cTLzII', 'AE7xKk', 'FtkDMy', 'TkQuHF', 'Zqx2gw', 'LbAjaI', 'rao4KK', 'aH5Dtg', 'dbGgGg', 'LkOM9Y', 'QEA8a8', 'Qadkgy', 'aXg9KI', 'nGLzOJ', 'yTqaYe', 'irnFKd', 'pJzjUt', 'w4bgNR', 'LWwJAo', 'BHVA24', 'btQfPF', 'wzldxs', 'rIhZPZ', 'XJj8D0', 'qDCJXQ', 'bZw1Ek', 'y0wVo3']

# Initialize a Rater object for each rater
raters = {}
for rater_id in rater_ids:
  raters[rater_id] = Rater(rater_id)

# First Pass
# Average everyone's ratings together, but ignore raters whose mean reliability
# rating is > 100.
all_distances, all_counts, all_rater_n, ka_data = AverageRatings(None, 100, None, False)

# Second Pass
# Average everyone's ratings together again, this time filtering out raters whose
# agreement with the average ratings of all raters in the first pass is < 0.4.
reliable_distances, reliable_counts, reliable_rater_n, ka_data = AverageRatings(0.4, 100, all_distances, True)

# Calculate Krippendorff's alpha - this is very slow
#print(Krippendorff.alpha(ka_data))
