#! /usr/bin/env python

from numpy import log2

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]

def entropy(X):
  P = probabilities(X)
  return 0.0-sum([p*log2(p) for p in P])

def conditionalEntropy(X, M):
  PX = probabilities(X)
  Y = range(0,48)
  return 0.0-sum([M[x][y]*log2(M[x][y]/PX[x]) for x in X.keys() for y in Y])

def probabilities(dic):
  tot = float(sum(dic.values()))
  probs = []
  for key in dic.keys():
    probs.append(dic[key] / tot)
  return probs

def jointProbabilities(experiment, chain, generation, set_type):
  W = getWords(experiment, chain, generation, set_type)
  U = set(W)
  n = float(len(W))
  probs = {}
  for u in U:
    row = []
    for i in range(0, 48):
      row.append(W.count(u) / n)
    probs[u] = row
  return probs
  

def countNGrams(experiment, chain, generation, set_type):
  W = getWords(experiment, chain, generation, set_type)
  longest_string = len(max(W))
  ngrams = [{} for i in range(0, longest_string)]
  for w in W:
    for i in range(1, longest_string+1):
      if len(w) >= i:
        for j in range(0, len(w)-i+1):
          gram = w[j:j+i]
          if gram in ngrams[i-1].keys():
            ngrams[i-1][gram] += 1
          else:
            ngrams[i-1][gram] = 1
  return ngrams

def countWords(experiment, chain, generation, set_type):
  W = getWords(experiment, chain, generation, set_type)
  word_count = {}
  for w in W:
    if w in word_count.keys():
      word_count[w] += 1
    else:
      word_count[w] = 1
  return word_count

def getWords(experiment, chain, generation, set_type):
  if set_type == "c":
    data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
  else:
    data = load(experiment, chain, generation, set_type)
  return [data[x][0] for x in range(0,len(data))]

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
