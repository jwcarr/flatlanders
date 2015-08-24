import numpy as np
import basics
import geometry

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]
segmentation_rules = [['ei', 'EY'],['oo','UW'], ['ai', 'AY'], ['ae', 'AY'], ['au', 'AW'], ['oi', 'OY'], ['iu', 'IY|UW'], ['oa', 'OW|AA'], ['o', 'OW'], ['ia', 'IY|AA'], ['ua', 'UW|AA'], ['ou', 'OW|UW'], ['i', 'IY'], ['a', 'AA'],['e', 'EY'], ['u', 'UW'], ['ch', 'C'], ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'], ['b', 'b'], ['d', 'd'], ['f','f'],['g','g'], ['h','h'], ['j','J'], ['k','k'], ['l','l'], ['m','m'], ['n','n'], ['p','p'], ['r','r'], ['s','s'], ['t','t'], ['v','v'], ['w','w'], ['y','y'], ['z','z'], ['x','k|s'], ['d|y','d|IY'], ['k|y','k|IY'], ['z|y','z|IY'], ['OW|r','AO|r']]
rounded_phonemes = ['b', 'd', 'g', 'l', 'm', 'n', 'N', 'OW', 'AO', 'UW']
pointed_phonemes = ['EY', 'IY', 'k', 'p', 't']

########################################

def experiment_sound_symbolism(experiment, set_type='s'):
  experiment_results = []
  for chain in chain_codes[experiment-1]:
    experiment_results.append(chain_sound_symbolism(experiment, chain, set_type))
  return experiment_results

def chain_sound_symbolism(experiment, chain, set_type='s'):
  chain_results = []
  for generation in range(0, 11):
    chain_results.append(generation_sound_symbolism(experiment, chain, generation, set_type))
  return chain_results

def generation_sound_symbolism(experiment, chain, generation, set_type):
  words = basics.getWords(experiment, chain, generation, set_type)
  triangles = basics.getTriangles(experiment, chain, generation, set_type)
  return correlate_roundedness_equilateralness(words, triangles)[0]

def correlate_roundedness_equilateralness(words, triangles, plot=False):
  word_scores = []
  for word in words:
    word_scores.append(word_roundedness(word))
  triangle_scores = []
  for triangle in triangles:
    triangle_scores.append(equilateralness(triangle))
  if plot == True:
    plt.scatter(word_scores, triangle_scores)
    plt.show()
  return np.corrcoef(word_scores, triangle_scores)[0,1]

########################################

def roundedness(word):
  segmented_word = segment_word(word)
  rounded_index = 0
  for phoneme in segmented_word:
    if phoneme in rounded_phonemes:
      rounded_index += 1
    elif phoneme in pointed_phonemes:
      rounded_index -= 1
  return rounded_index

def segment_word(word):
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
      if row[i] > 0:
        positive += 1
      total += 1
  return float(positive) / float(total)
