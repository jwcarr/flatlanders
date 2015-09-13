import basics

def experiment_results(experiment, set_type='s'):
  results = []
  for chain in basics.chain_codes[experiment-1]:
    results.append(chain_results(chain, set_type, experiment))
  dataset = {'data':results, 'experiment': experiment, 'starting_generation':0, 'data_type':'expressivity_' + set_type}
  return dataset

def chain_results(chain, set_type='s', experiment=False):
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  results = []
  for generation in range(0, 11):
    results.append(generation_results(chain, generation, set_type, experiment))
  return results

def generation_results(chain, generation, set_type='s', experiment=False):
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  return basics.uniqueStrings(experiment, chain, generation, set_type)
