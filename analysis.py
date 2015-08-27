#! /usr/bin/env python
# encoding: utf-8

from random import shuffle
from scipy import log, log2, mean, polyfit, sqrt, stats, std
from string import ascii_uppercase
import matplotlib.pyplot as plt
import scipy.cluster
import re
import numpy
import math
import basics
import Mantel
import MantelCategorical
import Page
import svg_polygons
import rater_analysis as ra

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]

def expressivity(experiment, set_type):
  results = []
  for chain in chain_codes[experiment-1]:
    scores = []
    for generation in range(0, 11):
      score = basics.uniqueStrings(experiment, chain, generation, set_type)
      scores.append(score)
    results.append(scores)
  return results

#############################################################################
# MEASURE LEARNABILITY: CALCULATE TRANSMISSION ERROR AND THEN COMPARE THE
# VERIDICAL SCORE TO A MONTE CARLO SAMPLE

def learnability(experiment, chain, generation, simulations=100000):
  words_A = basics.getWords(experiment, chain, generation, "s")
  words_B = basics.getWords(experiment, chain, generation-1, "s")
  x = basics.meanNormLevenshtein(words_A, words_B)
  m, sd = MonteCarloError(words_A, words_B, simulations)
  z = (m-x)/sd
  return x, m, sd, z

# CALCULATE THE TRANSMISSION ERROR BETWEEN TWO CONSECUTIVE PARTICIPANTS

def transmissionError(experiment, chain, generation):
  words_A = basics.getWords(experiment, chain, generation, "s")
  words_B = basics.getWords(experiment, chain, generation-1, "s")
  return basics.meanNormLevenshtein(words_A, words_B)

# GIVEN TWO SETS OF STRINGS, SHUFFLE ONE SET OF STRINGS n TIMES. COMPUTE THE
# MEAN NORMALIZED LEVENSHTEIN DISTANCE FOR EACH SHUFFLING AND RETURN THE MEAN
# AND STANDARD DEVIATION OF THE COMPUTED SCORES

def MonteCarloError(strings1, strings2, simulations):
  distances = []
  for i in xrange(0, simulations):
    shuffle(strings1)
    distances.append(basics.meanNormLevenshtein(strings1, strings2))
  return mean(distances), std(distances)

#############################################################################
# GET TRANSMISSION ERROR RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allTransmissionErrors(experiment):
  results = []
  for chain in chain_codes[experiment-1]:
    scores = []
    for generation in range(1, 11):
      try:
        score = transmissionError(experiment, chain, generation)
        scores.append(score)
      except:
        scores.append("N/A")
    results.append(scores)
  return results

#############################################################################
# GET LEARNABILITY RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allLearnability(experiment, sims=100000):
  results = []
  for chain in chain_codes[experiment-1]:
    print "Chain " + chain + "..."
    scores = []
    for generation in range(1, 11):
      try:
        score = learnability(experiment, chain, generation, sims)[3]
        scores.append(score)
      except:
        scores.append(None)
    results.append(scores)
  return results

#############################################################################
# GET TRANSMISSION ERROR RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allTrainingErrors(experiment):
  results = []
  for chain in chain_codes[experiment-1]:
    scores = []
    for generation in range(1, 11):
      try:
        score = basics.trainingError(experiment, chain, generation)
        scores.append(score)
      except:
        scores.append("N/A")
    results.append(scores)
  return results

#############################################################################
# CALCULATE COMMUNICATIVE ACCURACY

def commAccuracy(chain, generation):
  dynamic_set = basics.load(3, chain, generation, "d")
  static_set = basics.load(3, chain, generation, "s")
  target_triangles = []
  select_triangles = []
  for item in dynamic_set+static_set:
    target_triangle = []
    select_triangle = []
    for i in [1,2,3]:
      x, y = item[i].split(',')
      target_triangle.append([int(x), int(y)])
      x, y = item[i+4].split(',')
      select_triangle.append([int(x), int(y)])
    target_triangles.append(target_triangle)
    select_triangles.append(select_triangle)
  target_triangles = numpy.asarray(target_triangles, dtype=float)
  select_triangles = numpy.asarray(select_triangles, dtype=float)
  target_features = meaning_space.MakeFeatureMatrix(target_triangles, False)
  select_features = meaning_space.MakeFeatureMatrix(select_triangles, False)
  accuracy = 0.0
  correct = 0.0
  for i in range(0, len(target_features)):
    acc = meaning_space.ED(target_features[i], select_features[i])
    accuracy += acc
    if acc == 0.0:
      correct += 1
  return accuracy / len(target_features), correct

#############################################################################
# RUN ALL THREE STATS

def runStats(data_matrix, hypothesis="d", include_gen_zero=True):

  if include_gen_zero == False:
    matrix = []
    for row in data_matrix:
      matrix.append([row[i] for i in range(1,len(row))])
  else:
    matrix = data_matrix

  page_results = page.ptt(matrix, hypothesis)
  print('''Page's trend test
L = %s, m = %s, n = %s, p %s, one-tailed''' % page_results)
  print("")

  pearson_results = pearson(matrix)
  print('''Correlation between scores and generation numbers
r = %s, n = %s, p = %s, one-tailed''' % pearson_results)
  print("")

  student_results = student(matrix, hypothesis)
  print('''Paired t-test between first and last generations
diff = %s, t (%s) = %s, p = %s, one-tailed''' % student_results)

#############################################################################
# CORRELATE A MATRIX OF RESULTS WITH GENERATION NUMBERS

def pearson(matrix):
  scores = matrix2vector(matrix)
  gen_nums = range(1,len(matrix[0])+1)*len(matrix)
  test = stats.pearsonr(scores, gen_nums)
  return test[0], len(scores), test[1]/2.0

#############################################################################
# PAIRED T-TEST BETWEEN FIRST AND LAST GENERATIONS

def student(matrix, hypothesis):
  a = [row[0] for row in matrix]
  b = [row[len(matrix[0])-1] for row in matrix]
  if hypothesis == "ascending" or hypothesis == "a":
    test = stats.ttest_rel(b, a)
    diff = (float(sum(b))/len(b)) - (float(sum(a))/len(a))
  if hypothesis == "descending" or hypothesis == "d":
    test = stats.ttest_rel(a, b)
    diff = (float(sum(a))/len(a)) - (float(sum(b))/len(b))
  return diff, len(a)-2, test[0], test[1]/2.0

#############################################################################
# CONVERT MATRIX INTO VECTOR

def matrix2vector(matrix):
  vector = []
  for row in matrix:
    for cell in row:
      vector.append(cell)
  return vector

#############################################################################
# GET STRUCTURE SCORES FOR ALL CHAINS IN AN EXPERIMENT

def allStructureScores(experiment, sims=1000, meaning_distances=False):
  if type(meaning_distances) == bool and meaning_distances == False:
    meaning_distances = ra.reliable_distance_array
  matrix = []
  for chain in chain_codes[experiment-1]:
    print "  Chain " + chain + "..."
    scores = []
    for generation in range(0, 11):
      score = None
      if basics.uniqueStrings(experiment, chain, generation, 's') > 1:
        score = structureScore(experiment, chain, generation, sims, meaning_distances)
      scores.append(score)
    matrix.append(scores)
  return matrix

#############################################################################
# CORRELATE THE STRING EDIT DISTANCES AND MEANING DISTANCES, THEN RUN THE
# DISTANCES THROUGH A MONTE CARLO SIMULATION. RETURN THE VERDICAL COEFFICIENT,
# THE MEAN AND STANDARD DEVIATION OF THE MONTE CARLO SAMPLE, AND THE Z-SCORE

def structureScore(experiment, chain, generation, simulations=1000, meaning_distances=False):
  strings = basics.getWords(experiment, chain, generation, 's')
  string_distances = basics.stringDistances(strings)
  if type(meaning_distances) == bool and meaning_distances == False:
    meaning_distances = ra.reliable_distance_array
  z = Mantel.Test(string_distances, meaning_distances, simulations)[2]
  return z


#############################################################################
# GET CATEGORICAL STRUCTURE SCORES FOR ALL CHAINS IN AN EXPERIMENT

def allCatStructureScores(experiment, sims=1000):
  matrix = []
  for chain in chain_codes[experiment-1]:
    print "  Chain " + chain + "..."
    scores = []
    for generation in range(0, 11):
      score = None
      if basics.uniqueStrings(experiment, chain, generation, 's') > 2:
        score = MantelCategorical.Test(experiment, chain, generation, 's', sims)[3]
      scores.append(score)
    matrix.append(scores)
  return matrix

#############################################################################
# CALCULATE THE ENTROPY OF A LANGUAGE

def entropy(experiment, chain, generation):
  P = syllableProbabilities(experiment, chain, generation)
  return 0.0-sum([p*log2(p) for p in P.values()])

#############################################################################
# CALCULATE THE CONDITIONAL ENTROPY OF A LANGUAGE

def conditionalEntropy(experiment, chain, generation):
  X, Y, M = bisyllableProbabilities(experiment, chain, generation)
  N = float(len(X))
  return 0.0-sum([M[x][y]*log2(M[x][y]/(X[x]/N)) for x in X.keys() for y in Y.keys()])

#############################################################################
# GET SYLLABLE PROBABILITIES

def syllableProbabilities(experiment, chain, generation, start_stop=False):
  words = basics.getWords(experiment, chain, generation, "d")
  segmented_words = segment(words, start_stop)
  syllables = {}
  for word in segmented_words:
    for syllable in word:
      if syllable in syllables.keys():
        syllables[syllable] += 1.0
      else:
        syllables[syllable] = 1.0
  N = float(sum(syllables.values()))
  for s in syllables.keys():
    syllables[s] = syllables[s]/N
  return syllables

def condEnt(experiment, chain, generation):
  syllables = syllableProbabilities(experiment, chain, generation, True)
  bisyllables = bisyllableProbabilities(experiment, chain, generation, True)
  H = 0.0
  for x in syllables.keys():
    p_x = syllables[x]
    total = 0.0
    for y in syllables.keys():
      if bisyllables.has_key(x+y) == True:
        p_xy = bisyllables[x+y]
        total += p_xy*log2(p_xy)
    H += (p_x * total)
  return -H

def bisyllableProbabilities(experiment, chain, generation, start_stop=True):
  words = basics.getWords(experiment, chain, generation, "d")
  segmented_words = segment(words, start_stop)
  bisyllables = {}
  for word in segmented_words:
    for i in range(0,len(word)-1):
      bisyll = "".join(word[i:i+2])
      if bisyll in bisyllables.keys():
        bisyllables[bisyll] += 1.0
      else:
        bisyllables[bisyll] = 1.0
  N = float(sum(bisyllables.values()))
  for s in bisyllables.keys():
    bisyllables[s] = bisyllables[s]/N
  return bisyllables

#############################################################################
# SEGMENT WORDS INTO THEIR COMPONENT SYLLABLES

#rules = [['zwac','zwAA'],['wac', 'wAA'],['ei', 'EY'],['oo','UW'],['or', 'AOr'],['ai', 'AY'],['ae', 'AY'],
 #      ['au', 'AW'],['oi', 'OY'],['o', 'OW'],['i', 'IY'],['a', 'AA'],
 #      ['e', 'EH'],['u', 'UW'],['ch', 'C'],['j', 'J'],['ck', 'k'],
  #     ['c', 'k'],['ng', 'N'],['sh', 'S'],['th', 'T']]

rules = [['ei', 'EY'],['oo','UW'], ['or', 'AOr'], ['ai', 'AY'], ['ae', 'AY'],
         ['au', 'AW'], ['oi', 'OY'], ['iu', 'IWUW'], ['oa', 'OWAA'],
         ['o', 'OW'], ['ia', 'IYAA'], ['ua', 'UWAA'], ['ou', 'OWUW'],
         ['i', 'IY'], ['a', 'AA'],['e', 'EY'], ['u', 'UW'], ['ch', 'C'],
         ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'],
         ['zz', 'z'], ['pp', 'p'], ['kk','k'],['dd','d']]

def segment(words, start_stop=False):
  segmented_words = []
  for i in range(0,len(words)):
    for rule in rules:
      words[i] = words[i].replace(rule[0], rule[1]+"|")
    if words[i][-1] == "|":
      words[i] = words[i][:-1]
    segmented_words.append(words[i].split("|"))
  for i in segmented_words:
    for j in range(0, len(i)):
      if len(i[j]) == 1:
        i[j-1] = i[j-1] + i[j]
        i.pop(j)
        j = j-1
    if start_stop == True:
      i.insert(0,"<")
      i.append(">")
  return segmented_words

def wordMemory(experiment, chain, generation):
  words_a = set(basics.getWords(experiment, chain, generation, 'c'))
  words_b = set(basics.getWords(experiment, chain, generation-1, 'd'))
  n = float(max(len(words_a),len(words_b)))
  return len(words_a.intersection(words_b))/n
