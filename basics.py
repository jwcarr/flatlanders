import numpy as np
from datetime import timedelta
from os import getenv

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]
desktop_location = getenv('HOME') + '/Desktop/'

# Determine which experiment number a chain belongs to
def determine_experiment_number(chain):
  for experiment in range(0, len(chain_codes)):
    if chain in chain_codes[experiment]:
      return experiment + 1
  return None

# Get the words for a given set
def getWords(experiment, chain, generation, set_type):
  if set_type == "c":
    data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
  else:
    data = load(experiment, chain, generation, set_type)
  return [data[x][0] for x in range(0,len(data))]

# Get the triangles for a given set
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
    triangles.append(np.array([[x1,y1],[x2,y2],[x3,y3]], dtype=float))
  return triangles

# Return a count of the number of unique strings in a given set
def uniqueStrings(experiment, chain, generation, set_type):
  if set_type == 's':
    words = getWords(experiment, chain, generation, 's')
  elif set_type == 'd':
    words = getWords(experiment, chain, generation, 'd')
  elif set_type == 'c':
    words = getWords(experiment, chain, generation, 's') + getWords(experiment, chain, generation, 'd')
  else:
    raise ValueError('Invalid set type. Should be "s", "d", or "c".')
  return len(set(words))

def allTrainingErrors(experiment):
  results = []
  for chain in basics.chain_codes[experiment-1]:
    scores = []
    for generation in range(1, 11):
      try:
        score = basics.trainingError(experiment, chain, generation)
        scores.append(score)
      except:
        scores.append("N/A")
    results.append(scores)
  return results

# Return the amount of training error made by a participant
def trainingError(experiment, chain, generation, subject=False):
  if subject == 'A' or subject == 'B':
    filename = 'logSub' + subject
  else:
    filename = 'log'
  data = load(experiment, chain, generation, filename)
  words_A = [data[x][0] for x in range(5,53)]
  words_B = [data[x][1] for x in range(5,53)]
  x = meanNormLevenshtein(words_A, words_B)
  return x

# Calculate the average amount of time spent on each test item
def timePerItem(experiment, chain, generation):
  set_d = load(experiment, chain, generation, "d")
  timestamp_1 = stringToTimeStamp(set_d[0][4])
  timestamp_50 = stringToTimeStamp(set_d[47][4])
  difference = timestamp_50 - timestamp_1
  time_per_item_set_d = difference.total_seconds() / 94.0
  return time_per_item_set_d

# Calcualte total time spent on the experiment
def timeSpent(experiment, chain, generation, subject=False):
  print experiment, chain, generation
  if subject == False:
    log_file = load(experiment, chain, generation, "log")
  else:
    log_file = load(experiment, chain, generation, 'logSub' + subject)
  if experiment == 3:
    start_time = stringToTimeStamp(log_file[1][4].split(" ")[1])
  else:
    start_time = stringToTimeStamp(log_file[1][3].split(" ")[1])
  if experiment == 2:
    end_time = stringToTimeStamp(log_file[56][0].split(" ")[3])
  else:
    end_time = stringToTimeStamp(log_file[54][0].split(" ")[3])
  difference = end_time - start_time
  return difference.total_seconds()

# Convert string to timestamp
def stringToTimeStamp(string):
  time = string.split(":")
  timestamp = timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))
  return timestamp

# Return number of times a participant was asked to choose new word (experiment 2 only)
def overuseCount(chain, generation, subject):
  if subject == 'A' or subject == 'B':
    filename = 'logSub' + subject
  else:
    filename = 'log'
  data = load(2, chain, generation, filename)
  line = str(data[54])
  split1 = line.split("overuse count = ")
  split2 = split1[1].split("'")
  return int(split2[0])

# Take a list of strings, conpute the distance between every pair, and return condensed distance matrix
def stringDistances(strings):
  distances = []
  for i in range(0,len(strings)):
    for j in range(i+1,len(strings)):
      distances.append(LevenshteinDistance(strings[i], strings[j]))
  return distances

# Compute mean normalized Levenshtein distance between consecutive static sets
def meanNormLevenshtein(strings1, strings2):
  total = 0.0
  for i in range(0, len(strings1)):
    total += LevenshteinDistance(strings1[i], strings2[i])
  return total/float(len(strings1))

def LevenshteinDistance(s1, s2):
  if len(s1) > len(s2):
    s1,s2 = s2,s1
  distances = range(len(s1) + 1)
  for index2, char2 in enumerate(s2):
    newDistances = [index2 + 1]
    for index1, char1 in enumerate(s1):
      if char1 == char2:
        newDistances.append(distances[index1])
      else:
        newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
    distances = newDistances
  return float(distances[-1])/max(len(s1), len(s2))

# Load in a data file
def load(experiment, chain, generation, set_type):
  filename = "data/" + str(experiment) + "/" + chain + "/" + str(generation) + set_type
  f = open(filename, 'r')
  data = f.read()
  f.close()
  return [row.split('\t') for row in data.split('\n')]

# Write out a matrix to a file on the desktop
def writeOut(matrix, filename='file'):
  data = ""
  for row in matrix:
    row = [str(x) for x in row]
    data = data + "\t".join(row) + "\n"
  data = data[0:-1]
  f = open(desktop_location + filename, 'w')
  f.write(data)
  f.close()

# Read in a previously saved data file to a matrix
def readIn(filename):
  f = open(filename, 'r')
  data = f.read()
  f.close()
  lines = data.split("\n")
  matrix = []
  for line in lines:
    cells = line.split("\t")
    row = []
    for cell in cells:
      try:
        cell = float(cell)
      except:
        cell = None
      row.append(cell)
    matrix.append(row)
  return matrix
