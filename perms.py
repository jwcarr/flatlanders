import numpy as np
import meaning_space

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]

feature_space = meaning_space.MakeFeatureMatrix(1, "A", 0, "s")

def feature_slice(dimensions):
  return [[row[i] for i in dimensions] for row in feature_space]

def condense(matrix):
  n = len(matrix)
  dist_vector = []
  for i in range(0, n):
    for j in range(i+1, n):
      dist_vector.append(ED(matrix[i], matrix[j]))
  return dist_vector

def ED(a, b):
  return np.sqrt(sum([(a[i]-b[i])**2 for i in range(0, len(a))]))

def correlate(string_distances, feature_dimensions):
  return np.corrcoef(string_distances, condense(feature_slice(feature_dimensions)))[0,1]

def run(experiment):
  experiment_results = []
  for chain in chain_codes[experiment-1]:
    chain_results = []
    for generation in range(0,11):
      generation_results = []
      string_distances = meaning_space.stringDistances(meaning_space.getWords(experiment, chain, generation, 's'))
      for i in range(0, 18):
        generation_results.append([correlate(string_distances, [i]), [i]])
        for j in range(i+1, 18):
          generation_results.append([correlate(string_distances, [i,j]), [i,j]])
          for k in range(j+1, 18):
            generation_results.append([correlate(string_distances, [i,j,k]), [i,j,k]])
            for l in range(k+1, 18):
              generation_results.append([correlate(string_distances, [i,j,k,l]), [i,j,k,l]])
              for m in range(l+1, 18):
                generation_results.append([correlate(string_distances, [i,j,k,l,m]), [i,j,k,l,m]])
                for n in range(m+1, 18):
                  generation_results.append([correlate(string_distances, [i,j,k,l,m,n]), [i,j,k,l,m,n]])
                  for o in range(18, 18):
                    generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o]), [i,j,k,l,m,n,o]])
                    for p in range(o+1, 18):
                      generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p]), [i,j,k,l,m,n,o,p]])
                      for q in range(p+1, 18):
                        generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q]), [i,j,k,l,m,n,o,p,q]])
                        for r in range(q+1, 18):
                          generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r]), [i,j,k,l,m,n,o,p,q,r]])
                          for s in range(r+1, 18):
                            generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s]), [i,j,k,l,m,n,o,p,q,r,s]])
                            for t in range(s+1, 18):
                              generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t]), [i,j,k,l,m,n,o,p,q,r,s,t]])
                              for u in range(t+1, 18):
                                generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t,u]), [i,j,k,l,m,n,o,p,q,r,s,t,u]])
                                for v in range(u+1, 18):
                                  generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t,u,v]), [i,j,k,l,m,n,o,p,q,r,s,t,u,v]])
                                  for w in range(v+1, 18):
                                    generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w]), [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w]])
                                    for x in range(w+1, 18):
                                      generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x]), [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x]])
                                      for y in range(x+1, 18):
                                        generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y]), [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y]])
                                        for z in range(y+1, 18):
                                          generation_results.append([correlate(string_distances, [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]), [i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]])
      chain_results.append(generation_results)
    experiment_results.append(chain_results)
  return experiment_results

def sum_correlations(results):
  dims = dict(zip(range(0,18), [0.0] * 18))
  for i in results:
    corr = i[0]
    for j in i[1]:
      dims[j] += corr
  return dims










