#!/usr/bin/env python

from random import randrange

def assign(chain_codes, start_gen, end_gen):
  chain_gens = {}
  for chain in chain_codes:
    chain_gens[chain] = range(start_gen, end_gen+1)
  random_assignment = []
  for i in range(0, len(chain_codes)*(end_gen-start_gen+1)):
    code = chain_codes[randrange(0, len(chain_codes))]
    gen = chain_gens[code][0]
    del chain_gens[code][0]
    if len(chain_gens[code]) == 0:
      chain_codes.remove(code)
    random_assignment.append( code+str(gen) )
  return random_assignment
