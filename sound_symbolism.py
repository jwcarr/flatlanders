from math import isnan
import numpy as np
import basics
import geometry

########################################

# Rules describing how to translate graphemes to phonemes
segmentation_rules = [['ei', 'EY'],['oo','UW'], ['ai', 'AY'], ['ae', 'AY'], ['au', 'AW'], ['oi', 'OY'], ['iu', 'IY|UW'], ['oa', 'OW|AA'], ['o', 'OW'], ['ia', 'IY|AA'], ['ua', 'UW|AA'], ['ou', 'OW|UW'], ['i', 'IY'], ['a', 'AA'],['e', 'EY'], ['u', 'UW'], ['ch', 'C'], ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'], ['b', 'b'], ['d', 'd'], ['f','f'],['g','g'], ['h','h'], ['j','J'], ['k','k'], ['l','l'], ['m','m'], ['n','n'], ['p','p'], ['r','r'], ['s','s'], ['t','t'], ['v','v'], ['w','w'], ['y','y'], ['z','z'], ['x','k|s'], ['d|y','d|IY'], ['k|y','k|IY'], ['z|y','z|IY'], ['OW|r','AO|r']]

# Sets of phonemes associated with rounded/pointed and big/small stimuli
roundedness_phonemes = [['b', 'd', 'g', 'l', 'm', 'n', 'N', 'OW', 'AO', 'UW'], ['EY', 'IY', 'k', 'p', 't']]
bigness_phonemes = [['b', 'd', 'g', 'l', 'm', 'w', 'AA', 'OW', 'AO', 'UW'], ['k', 'p', 't', 'EY', 'IY']]

########################################

# Functions for generating experiment, chain, or generation results

def experiment_sound_symbolism(experiment, set_type='s', symbolism='shape'):
  experiment_results = []
  for chain in basics.chain_codes[experiment-1]:
    experiment_results.append(chain_sound_symbolism(experiment, chain, set_type, symbolism))
  return experiment_results

def chain_sound_symbolism(experiment, chain, set_type='s', symbolism='shape'):
  chain_results = []
  for generation in range(0, 11):
    chain_results.append(generation_sound_symbolism(experiment, chain, generation, set_type, symbolism))
  return chain_results

def generation_sound_symbolism(experiment, chain, generation, set_type, symbolism='shape'):
  words = basics.getWords(experiment, chain, generation, set_type)
  triangles = basics.getTriangles(experiment, chain, generation, set_type)
  if symbolism == 'shape':
    return correlate_form_and_symbolism(words, roundedness_phonemes, triangles, geometry.equilateralness)
  elif symbolism == 'size':
    return correlate_form_and_symbolism(words, bigness_phonemes, triangles, geometry.area)
  else:
    raise ValueError('Invalid symbolism argument. Should be "shape" or "size".')

########################################

# Given words and a list of sound symbolic phonemes, and triangles and triangle
# metric, correlate the scores

def correlate_form_and_symbolism(words, symbolic_phonemes, triangles, triangle_metric):
  word_scores = [score_word(word, symbolic_phonemes) for word in words]
  triangle_scores = [triangle_metric(triangle) for triangle in triangles]
  return np.corrcoef(word_scores, triangle_scores)[0,1]

# Score a word using a list of sound symbolic phonemes

def score_word(word, symbolic_phonemes):
  segmented_word = segment(word)
  score = 0
  for phoneme in segmented_word:
    if phoneme in symbolic_phonemes[0]:
      score += 1
    elif phoneme in symbolic_phonemes[1]:
      score -= 1
  return score

# Segment a word into a list of phonemes

def segment(word):
  for rule in segmentation_rules:
    word = word.replace(rule[0], rule[1]+'|')
  word = word.replace('||', '|')
  if word[-1] == '|':
    word = word[:-1]
  return word.split('|')

########################################

# Calculate the proportion of correlation coefficients that are positive
# Pass in the results from experiment_sound_symbolism()

def percent_positive(matrix):
  positive = 0
  total = 0
  for row in matrix:
    for i in range(1,len(row)):
      if isnan(row[i]) == True:
        continue
      if row[i] > 0:
        positive += 1
      total += 1
  return positive, total, float(positive) / float(total)
