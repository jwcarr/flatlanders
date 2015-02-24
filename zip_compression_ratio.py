#! /usr/bin/env python

from subprocess import call
from os import path

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]

def load(experiment, chain, generation, set_type):
  filename = "Data/" + str(experiment) + "/" + chain + "/" + str(generation) + set_type
  f = open(filename, 'r')
  data = f.read()
  f.close()
  rows = data.split("\n")
  matrix = []
  for row in rows:
    cells = row.split("\t")
    matrix.append(cells)
  return matrix

def getWords(experiment, chain, generation, set_type):
  if set_type == "c":
    data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
  else:
    data = load(experiment, chain, generation, set_type)
  return [data[x][0] for x in range(0,len(data))]

def compressionRatio(experiment, chain, generation, set_type):
  W = getWords(experiment, chain, generation, set_type)
  writeWords(W, "temp")
  before = float(path.getsize("temp"))
  call(["gzip", "temp"])
  after = float(path.getsize("temp.gz"))
  call(["rm", "temp.gz"])
  return before / after

def writeWords(words, filename):
  data = '\n'.join(words)
  f = open(filename, 'w')
  f.write(data)
  f.close()