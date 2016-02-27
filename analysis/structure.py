import sublexical_structure
import Mantel
import basics
import rater_analysis

def experiment_results(experiment, sublexical=False, permutations=1000, meaning_distances=False):
  if type(meaning_distances) == bool and meaning_distances == False:
    meaning_distances = rater_analysis.reliable_distance_array
  results = []
  for chain in basics.chain_codes[experiment-1]:
    print('Chain ' + chain + '...')
    results.append(chain_results(chain, sublexical, permutations, meaning_distances, experiment))
  if sublexical == True:
    dataset = {'data':results, 'experiment':experiment, 'starting_generation':0,
      'y_range':(-3,14), 'y_label':'Sublexical structure', 'data_type':'sublexical_structure'}
  else:
    dataset = {'data':results, 'experiment':experiment, 'starting_generation':0,
      'y_range':(-3,14), 'y_label':'Structure', 'data_type':'structure'}
  return dataset

def chain_results(chain, sublexical=False, permutations=1000, meaning_distances=False, experiment=False):
  if type(meaning_distances) == bool and meaning_distances == False:
    meaning_distances = rater_analysis.reliable_distance_array
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  results = []
  for generation in range(0, 11):
    results.append(generation_results(chain, generation, sublexical, permutations, meaning_distances, experiment))
  return results

def generation_results(chain, generation, sublexical=False, permutations=1000, meaning_distances=False, experiment=False):
  if type(meaning_distances) == bool and meaning_distances == False:
    meaning_distances = rater_analysis.reliable_distance_array
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  strings = basics.getWords(experiment, chain, generation, 's')
  if len(set(strings)) > 1:
    if sublexical == True:
      return sublexical_structure.test(strings, meaning_distances, permutations)
    string_distances = basics.stringDistances(strings)
    return Mantel.test(string_distances, meaning_distances, permutations)[2]
  return None
