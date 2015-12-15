import basics

def experiment_results(experiment):
  results = [chain_results(chain, experiment) for chain in basics.chain_codes[experiment-1]]
  return {'data':results, 'experiment':experiment, 'starting_generation':0, 'data_type':'word_length'}

def chain_results(chain, experiment=False):
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  return [generation_results(chain, generation, experiment) for generation in range(0, 11)]

def generation_results(chain, generation, experiment=False):
  if type(experiment) == bool and experiment == False:
    experiment = basics.determine_experiment_number(chain)
  words = basics.getWords(experiment, chain, generation, 's')
  return sum([len(word) for word in words]) / float(len(words))
