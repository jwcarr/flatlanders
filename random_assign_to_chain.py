#!/usr/bin/env python

from random import randrange

def assign(chain_codes, generations):
  chain_gens = {}
  for chain in chain_codes:
    chain_gens[chain] = range(1, generations+1)
  random_assignment = []
  for i in range(0, len(chain_codes)*generations):
    code = chain_codes[randrange(0, len(chain_codes))]
    gen = chain_gens[code][0]
    del chain_gens[code][0]
    if len(chain_gens[code]) == 0:
      chain_codes.remove(code)
    random_assignment.append( code+str(gen) )
  return random_assignment
