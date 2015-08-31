import numpy as np
import basics
import geometry

########################################

# Rules describing how to translate graphemes to phonemes
segmentation_rules = [['ei', 'EY'],['oo','UW'], ['ai', 'AY'], ['ae', 'AY'], ['au', 'AW'], ['oi', 'OY'], ['iu', 'IY|UW'], ['oa', 'OW|AA'], ['o', 'OW'], ['ia', 'IY|AA'], ['ua', 'UW|AA'], ['ou', 'OW|UW'], ['i', 'IY'], ['a', 'AA'],['e', 'EY'], ['u', 'UW'], ['ch', 'C'], ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'], ['b', 'b'], ['d', 'd'], ['f','f'],['g','g'], ['h','h'], ['j','J'], ['k','k'], ['l','l'], ['m','m'], ['n','n'], ['p','p'], ['r','r'], ['s','s'], ['t','t'], ['v','v'], ['w','w'], ['y','y'], ['z','z'], ['x','k|s'], ['d|y','d|IY'], ['k|y','k|IY'], ['z|y','z|IY'], ['OW|r','AO|r']]

# Sets of phonemes associated with rounded/pointed and big/small stimuli
roundedness_phonemes = [['b', 'd', 'g', 'l', 'm', 'n', 'N', 'OW', 'AO', 'UW'], ['k', 'p', 't', 'EY', 'IY']]
bigness_phonemes = [['b', 'd', 'g', 'l', 'm', 'w', 'AA', 'OW', 'AO', 'UW'], ['k', 'p', 't', 'EY', 'IY']]

########################################

# Functions for generating experiment, chain, or generation results

def experiment_results(experiment, set_type='s', symbolism='shape', monte_carlo=False):
  experiment_results = []
  for chain in basics.chain_codes[experiment-1]:
    experiment_results.append(chain_results(experiment, chain, set_type, symbolism, monte_carlo))
  return experiment_results

def chain_results(experiment, chain, set_type='s', symbolism='shape', monte_carlo=False):
  chain_results = []
  for generation in range(0, 11):
    chain_results.append(generation_results(experiment, chain, generation, set_type, symbolism, monte_carlo))
  return chain_results

def generation_results(experiment, chain, generation, set_type, symbolism='shape', monte_carlo=False):
  words = basics.getWords(experiment, chain, generation, set_type)
  triangles = basics.getTriangles(experiment, chain, generation, set_type)
  if symbolism == 'shape':
    return correlate_form_and_symbolism(words, roundedness_phonemes, triangles, geometry.equilateralness, monte_carlo)
  elif symbolism == 'size':
    return correlate_form_and_symbolism(words, bigness_phonemes, triangles, geometry.centroid_size, monte_carlo)
  else:
    raise ValueError('Invalid symbolism argument. Should be "shape" or "size".')

########################################

# Given words and a list of sound symbolic phonemes, and triangles and a triangle
# metric, correlate the scores. If monte_carlo is False, just return the Pearson
# correlation coefficient, else use Monte_Carlo() and return a z-score.

def correlate_form_and_symbolism(words, symbolic_phonemes, triangles, triangle_metric, monte_carlo=False):
  word_scores = np.asarray([score_word(word, symbolic_phonemes) for word in words], dtype=int)
  triangle_scores = np.asarray([triangle_metric(triangle) for triangle in triangles], dtype=float)
  if type(monte_carlo) == int:
    return Monte_Carlo(word_scores, triangle_scores, monte_carlo)
  return np.corrcoef(word_scores, triangle_scores)[0,1]

# Given word scores and triangle scores, randomize the mapping between them a large
# number of times and compute a z-score for the significance of the veridical correlation

def Monte_Carlo(word_scores, triangle_scores, permutations):
  correlations = np.zeros(permutations, dtype=float)
  correlations[0] = np.corrcoef(word_scores, triangle_scores)[0,1]
  for i in range(1, permutations):
    np.random.shuffle(word_scores)
    correlations[i] = np.corrcoef(word_scores, triangle_scores)[0,1]
  return (correlations[0] - correlations.mean()) / correlations.std()

########################################

# Score a word using a list of sound symbolic phonemes

def score_word(word, symbolic_phonemes):
  segmented_word = segment_word(word)
  score = 0
  for phoneme in segmented_word:
    if phoneme in symbolic_phonemes[0]:
      score += 1
    elif phoneme in symbolic_phonemes[1]:
      score -= 1
  return score

# Segment a word into a list of phonemes

def segment_word(word):
  for rule in segmentation_rules:
    word = word.replace(rule[0], rule[1]+'|')
  word = word.replace('||', '|')
  if word[-1] == '|':
    word = word[:-1]
  return word.split('|')
