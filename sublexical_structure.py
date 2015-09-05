from itertools import permutations
from math import factorial
import numpy as np
import basics
import rater_analysis

# Run a categorical Mantel test. This is like a regular Mantel test, except that you're
# shuffling the categories that meanings belong to rather than shuffling the string-meaning
# mapping freely.

def test(experiment, chain, generation, set_type, randomizations):
  words = basics.getWords(experiment, chain, generation, set_type)
  word_distances = basics.stringDistances(words)
  categorized_words, categorized_meanings = CategorizeWords(words)
  meaning_distances = rater_analysis.reliable_distance_array
  r = np.corrcoef(meaning_distances, word_distances)[0,1]
  n = len(words)
  m, sd = Mantel(meaning_distances, categorized_words, categorized_meanings, r, n, generation, randomizations)
  z = (r-m)/sd
  return r, m, sd, z

# Takes a list of strings and returns two lists: a list of the unique strings, and another
# list of the same length which gives the meaning indices that the words map on to. Not using
# a dictionary because this can potentially create issues with the shuffling because
# dictionaries don't have order.

def CategorizeWords(words):
  categorized_words = []
  categorized_meanings = []
  for i in xrange(len(words)):
    try:
      position = categorized_words.index(words[i])
      categorized_meanings[position].append(i)
    except ValueError:
      categorized_words.append(words[i])
      categorized_meanings.append([i])
  return categorized_words, categorized_meanings

# If the number of possible mappings is less than the randomizations parameter, conduct a
# deterministic Mantel test; otherwise, do a stochasitc Mantel test.

def Mantel(meaning_distances, categorized_words, categorized_meanings, r, n, generation, randomizations):
  if factorial(len(categorized_words)) <= randomizations:
    print('    Generation %d: Only %d possible permutations - computing result deterministically' % (generation, factorial(len(categorized_words))))
    return DeterministicMantel(meaning_distances, categorized_words, categorized_meanings, n)
  return StochasticMantel(meaning_distances, categorized_words, categorized_meanings, r, n, randomizations)

# Stochasitc Mantel test - randomly sample the space of category-meaning mappings

def StochasticMantel(meaning_distances, categorized_words, categorized_meanings, r, n, randomizations):
  correlations = np.zeros(randomizations, dtype=float)
  correlations[0] = r
  for i in xrange(1, randomizations):
    correlations[i] = np.corrcoef(meaning_distances, GeneratePermutation(categorized_words, categorized_meanings, n))[0,1]
  return correlations.mean(), correlations.std()

def GeneratePermutation(categorized_words, categorized_meanings, n):
  np.random.shuffle(categorized_words)
  permuted_words = [None] * n
  for i in range(len(categorized_meanings)):
    for j in categorized_meanings[i]:
      permuted_words[j] = categorized_words[i]
  return basics.stringDistances(permuted_words)

# Deterministic Mantel test - measure every possible category-meaning mapping

def DeterministicMantel(meaning_distances, categorized_words, categorized_meanings, n):
  m = len(categorized_words)
  correlations = np.zeros(factorial(m), dtype=float)
  orders = permutations(range(m))
  i = 0
  for order in orders:
    correlations[i] = np.corrcoef(meaning_distances, GenerateDeterministicPermutation(categorized_words, categorized_meanings, order, n))[0,1]
    i += 1
  return correlations.mean(), correlations.std()

def GenerateDeterministicPermutation(categorized_words, categorized_meanings, order, n):
  permuted_words = [None] * n
  for i in range(len(categorized_meanings)):
    for j in categorized_meanings[i]:
      permuted_words[j] = categorized_words[order[i]]
  return basics.stringDistances(permuted_words)
