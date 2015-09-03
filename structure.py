import sublexical_structure
import Mantel
import basics
import rater_analysis
import plot as plt

def experiment_results(experiment, sublexical=False, permutations=1000, meaning_distances=False):
  if type(meaning_distances) == bool and meaning_distances == False:
    meaning_distances = rater_analysis.reliable_distance_array
  results = []
  for chain in basics.chain_codes[experiment-1]:
    print "  Chain " + chain + "..."
    results.append(chain_results(chain, sublexical, permutations, meaning_distances, experiment))
  return results

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
  if len(set(strings)) > 2:
    if sublexical == True:
      return MantelSublexical.test(experiment, chain, generation, 's', permutations)[3]
    string_distances = basics.stringDistances(strings)
    return Mantel.test(string_distances, meaning_distances, permutations)[2]
  return None

def plot(left_plot, right_plot, experiment, save_location=False):
  plt.chains(left_plot, dataset2=right_plot, miny=-2, maxy=14, y_label='Structure (z-score)', text='(A)', text2='(B)',  text_pos='top', experiment=experiment, conf=True, conf2=True, save_location=save_location, save_name='E%i_structure.pdf'%experiment)