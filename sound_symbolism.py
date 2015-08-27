from math import isnan
import numpy as np
import basics
import geometry

segmentation_rules = [['ei', 'EY'],['oo','UW'], ['ai', 'AY'], ['ae', 'AY'], ['au', 'AW'], ['oi', 'OY'], ['iu', 'IY|UW'], ['oa', 'OW|AA'], ['o', 'OW'], ['ia', 'IY|AA'], ['ua', 'UW|AA'], ['ou', 'OW|UW'], ['i', 'IY'], ['a', 'AA'],['e', 'EY'], ['u', 'UW'], ['ch', 'C'], ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'], ['b', 'b'], ['d', 'd'], ['f','f'],['g','g'], ['h','h'], ['j','J'], ['k','k'], ['l','l'], ['m','m'], ['n','n'], ['p','p'], ['r','r'], ['s','s'], ['t','t'], ['v','v'], ['w','w'], ['y','y'], ['z','z'], ['x','k|s'], ['d|y','d|IY'], ['k|y','k|IY'], ['z|y','z|IY'], ['OW|r','AO|r']]

rounded_phonemes = ['b', 'd', 'g', 'l', 'm', 'n', 'N', 'OW', 'AO', 'UW']
pointed_phonemes = ['EY', 'IY', 'k', 'p', 't']

big_phonemes = ['b', 'd', 'g', 'l', 'm', 'w', 'AA', 'OW', 'AO', 'UW']
small_phonemes = ['k', 'p', 't', 'EY', 'IY']

########################################

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
    return correlate_form_and_symbolism(words, roundedness, triangles, geometry.equilateralness)
  elif symbolism == 'size':
    return correlate_form_and_symbolism(words, bigness, triangles, geometry.area)
  else:
    raise ValueError('Invalid symbolism argument. Should be "shape" or "size".')

########################################

def correlate_form_and_symbolism(words, word_metric, triangles, triangle_metric):
  word_scores = [word_metric(word) for word in words]
  triangle_scores = [triangle_metric(triangle) for triangle in triangles]
  return np.corrcoef(word_scores, triangle_scores)[0,1]

########################################

def roundedness(word):
  segmented_word = segment(word)
  rounded_score = 0
  for phoneme in segmented_word:
    if phoneme in rounded_phonemes:
      rounded_score += 1
    elif phoneme in pointed_phonemes:
      rounded_score -= 1
  return rounded_score

def bigness(word):
  segmented_word = segment(word)
  bigness_score = 0
  for phoneme in segmented_word:
    if phoneme in big_phonemes:
      bigness_score += 1
    elif phoneme in small_phonemes:
      bigness_score -= 1
  return bigness_score

def segment(word):
  for rule in segmentation_rules:
    word = word.replace(rule[0], rule[1]+'|')
  word = word.replace('||', '|')
  if word[-1] == '|':
    word = word[:-1]
  return word.split('|')

########################################

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
