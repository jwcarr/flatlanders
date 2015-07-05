from scipy import array, random, stats, zeros
import meaning_space
import rater_analysis

def MantelTest(experiment, chain, generation, set_type, randomizations):
  words = meaning_space.getWords(experiment, chain, generation, set_type)
  meanings = meaning_space.MakeFeatureMatrix(experiment, chain, generation, set_type)
  meaning_distances = array(meaning_space.DistanceMatrix(meanings), dtype=float)
  r, p = stats.pearsonr(meaning_distances, word_distances)
  m, sd = MonteCarlo(meaning_distances, categorized_words, randomizations)
  z = (r-m)/sd
  return r, p, m, sd, z

def CategorizeWords(words):
  categorized_words = {}
  for i in xrange(len(words)):
    if words[i] in categorized_words.keys():
      categorized_words[words[i]].append(i)
    else:
      categorized_words[words[i]] = [i]
  return categorized_words

def MonteCarlo(meaning_distances, categorized_words, randomizations):
  correlations = zeros(randomizations, dtype=float)
  for i in xrange(randomizations):
    correlations[i] = stats.pearsonr(meaning_distances, GeneratePermutation(categorized_words))[0]
  return correlations.mean(), correlations.std()

def GeneratePermutation(categorized_words):
  words = categorized_words.keys()
  meanings = categorized_words.values()
  random.shuffle(words)
  permuted_categorization = dict(zip(words, meanings))
  permuted_words = [None] * 4
  for word in words:
    for meaning in permuted_categorization[word]:
      permuted_words[meaning] = word
  return meaning_space.stringDistances(permuted_words)
