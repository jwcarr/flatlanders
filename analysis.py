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
import meaning_space
import rater_analysis as ra

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]

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
        scores.append("N/A")
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

def allStructureScores(experiment, sims=1000):
  meaning_distances = ra.reliable_distance_array
  matrix = []
  for chain in chain_codes[experiment-1]:
    print "  Chain " + chain + "..."
    scores = []
    for generation in range(0, 11):
      score = None
      if basics.uniqueStrings(experiment, chain, generation)[1] > 1:
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
  if meaning_distances == False:
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

#############################################################################
# WRITE OUT A MATRIX TO A FILE ON THE DESKTOP

def writeOut(matrix, filename='file'):
  data = ""
  for row in matrix:
    row = [str(x) for x in row]
    data = data + "\t".join(row) + "\n"
  data = data[0:-1]
  f = open('/Users/jon/Desktop/' + filename + '.txt', 'w')
  f.write(data)
  f.close()

#############################################################################
# READ IN A PREVIOUSLY SAVED DATA FILE TO A MATRIX

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

def intergenCorr(experiment):
  ln_data = readIn("/Users/jon/Desktop/Experiment " +str(experiment) + " data/ln.txt")
  st_data = readIn("/Users/jon/Desktop/Experiment " +str(experiment) + " data/st.txt")
  y = matrix2vector(ln_data)
  x = matrix2vector(st_data)

  r, p = stats.pearsonr(x,y)
  n = len(x)
  print r, n, p
  m, b = polyfit(x, y, 1)
  ln = [(m*i)+b for i in range(-4,11)]

  fig, ax = plt.subplots(figsize=plt.figaspect(0.625))
  ax.scatter(x, y, marker="x", color='k', s=60)
  ax.plot(range(-4,11), ln, color="k", linewidth=2.0)
  plt.xlim(-4,10)
  plt.gcf().subplots_adjust(bottom=0.12)
  plt.xlabel("Structure score ($d_{T_{rm}}$) for generation $i-1$", fontsize=22)
  plt.ylim(-2,8)
  plt.ylabel("Learnability score for generation $i$", fontsize=22)
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  plt.show()

def allTriangleGraphics(experiment):
  T = basics.getTriangles(experiment, chain_codes[experiment-1][0], 0, "s")
  for chain in chain_codes[experiment-1]:
    for generation in range(0,11):
      words = basics.getWords(experiment, chain, generation, "s")
      unique_words = set(words)
      col = 0
      for word in unique_words:
        triangleGraphic(experiment, chain, generation, [word], True, False, col)
        col += 1
        if col == 11:
          col = 0

def wordMemory(experiment, chain, generation):
  words_a = set(basics.getWords(experiment, chain, generation, 'c'))
  words_b = set(basics.getWords(experiment, chain, generation-1, 'd'))
  n = float(max(len(words_a),len(words_b)))
  return len(words_a.intersection(words_b))/n

def soundSymbolism(experiment, chain, generation):
  words = basics.getWords(experiment, chain, generation, 'c')
  segmented_words = segment(words, False)
  T = basics.getTriangles(experiment, chain, generation, 'c')
  sounds = {'b':[], 'C':[], 'd':[], 'D':[], 'f':[], 'g':[], 'h':[], 'J':[], 'k':[], 'l':[], 'm':[], 'n':[], 'N':[], 'p':[], 'r':[], 's':[], 'S':[], 't':[], 'T':[], 'v':[], 'w':[], 'y':[], 'z':[], 'Z':[], 'AE':[], 'EY':[], 'AO':[], 'AX':[], 'IY':[], 'EH':[], 'IH':[], 'AY':[], 'AA':[], 'UW':[], 'UH':[], 'UX':[], 'OW':[], 'AW':[], 'OI':[]}
  for i in range(0,48):
    area_ratio = pointedness(T[i])
    theta = min([geometry.angle(T[i],1), geometry.angle(T[i],2), geometry.angle(T[i],3)])
    phon = "".join(segmented_words[i])
    for sound in sounds.keys():
      if phon.count(sound) > 0:
        sounds[sound].append(area_ratio)
    sound_counts = {}
    for sound in sounds.keys():
      if len(sounds[sound]) > 0:
        sound_counts[sound] = sum(sounds[sound])/float(len(sounds[sound]))
  return sound_counts

def pointedness(T):
  perimeter = geometry.perimeter(T)
  area = geometry.area(T)
  expected_area = (perimeter**2)/20.784609691
  return log(expected_area)/log(area)

def allSoundSymbolism(experiment,start_gen, end_gen):
  import pointedness
  ss  =[[soundSymbolism(experiment,x,y) for y in range(start_gen,end_gen)] for x in chain_codes[experiment-1]]
  ss_v = matrix2vector(ss)
  sounds = {'AA':[],'IY':[],'OW':[], 'UW':[], 'b':[], 'C':[], 'd':[], 'D':[], 'f':[], 'g':[], 'h':[], 'J':[], 'k':[], 'l':[], 'm':[], 'n':[], 'N':[], 'p':[], 'r':[], 's':[], 'S':[], 't':[], 'T':[], 'v':[], 'w':[], 'y':[], 'z':[], 'Z':[], 'AE':[], 'EY':[], 'AO':[], 'AX':[], 'EH':[], 'IH':[], 'AY':[], 'UH':[], 'UX':[], 'AW':[], 'OI':[]}
  for i in ss_v:
    for j in i.keys():
      sounds[j].append(i[j])
  matrix = []
  ipaLabels = ipaLabels = {'AA':u"ɑː",'IY':u"iː",'OW':u"əʊ", 'UW':u"uː", 'b':u"b", 'C':u"tʃ", 'd':u"d", 'D':u"ð", 'f':u"f", 'g':u"g", 'h':u"h", 'J':u"dʒ", 'k':u"k", 'l':u"l", 'm':u"m", 'n':u"n", 'N':u"ŋ", 'p':u"p", 'r':u"r", 's':u"s", 'S':u"ʃ", 't':u"t", 'T':u"θ", 'v':u"v", 'w':u"w", 'y':u"j", 'z':u"z", 'Z':u"ʒ", 'AE':u"a", 'EY':u"eɪ", 'AO':u"ɔː", 'AX':u"ə", 'EH':u"ɛ", 'IH':u"ɪ", 'AY':u"ʌɪ", 'UH':u"ə", 'UX':u"ʌ", 'AW':u"aʊ", 'OI':u"ɔɪ"}
  expected = pointedness.run(10000)
  for i in sounds.keys():
    if len(sounds[i]) > 20:
      mw = scipy.stats.mannwhitneyu(expected, sounds[i])
      matrix.append([ipaLabels[i], mean(sounds[i]), std(sounds[i]), (std(sounds[i])/sqrt(len(sounds[i])))*1.959964, mw[0], mw[1]*2])
  return matrix

def plotSoundSymbolism(matrix, y_label="Pointedness", miny=0.0, maxy=2, baseline=False):
  fig, ax = plt.subplots(figsize=plt.figaspect(0.625))
  n = len(matrix)
  if baseline == True:
    ax.plot(range(-1,n+1), [0.85]*(n+2), color='gray', linestyle=':')
  xvals = range(0,n)
  means = [row[1] for row in matrix]
  errors = [row[3] for row in matrix]
  pvals = [row[5] for row in matrix]
  (_, caps, _) = ax.errorbar(xvals, means, fmt="o", yerr=errors, color='k', linestyle="", linewidth=2.0, capsize=5.0, elinewidth=1.5)
  for cap in caps:
    cap.set_markeredgewidth(2)
  for i in xvals:
    sig = ""
    if pvals[i] <= 0.001:
      sig = "***"
    elif pvals[i] <= 0.01:
      sig = "**"
    elif pvals[i] <= 0.05:
      sig = "*"
    ax.annotate(sig, xy=(i,means[i]+errors[i]+0.05), zorder=10, color="red")
  labels = [row[0] for row in matrix]
  plt.xticks(xvals, labels, fontsize=14)
  plt.yticks(fontsize=14)
  plt.xlim(-0.5, n-0.5)
  plt.ylim(miny, maxy)
  plt.xlabel("Sounds", fontsize=22)
  plt.ylabel(y_label, fontsize=22)
  plt.show()
