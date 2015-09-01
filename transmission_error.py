import basics
import plot as plt

def experiment_results(experiment):
  results = []
  for chain in basics.chain_codes[experiment-1]:
    results.append(chain_results(chain, experiment))
  return results

def chain_results(chain, experiment=False):
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  results = []
  for generation in range(1, 11):
    results.append(generation_results(chain, generation, experiment))
  return results

def generation_results(chain, generation, experiment=False):
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  words_A = basics.getWords(experiment, chain, generation, "s")
  words_B = basics.getWords(experiment, chain, generation-1, "s")
  return basics.meanNormLevenshtein(words_A, words_B)

def plot(data, experiment, save_location=False):
  plt.chains(data, miny=0, maxy=1, y_label='Transmission error', experiment=experiment, save_location=save_location, save_name='E%i_transmission_error.pdf'%experiment)