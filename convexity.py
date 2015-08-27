from numpy import array, mean, median, sqrt, std
from random import shuffle
import basics

def allConvexity(experiment, Euclidean=True, iterations=100):
    return [[convexity(experiment, chain, gen, 's', Euclidean, iterations)[1] for gen in range(1,11)] for chain in basics.chain_codes[experiment-1]]

def convexity(experiment, chain, gen, set_type, Euclidean=True, iterations=100):
    T = meaning_space.MakePCAMatrix(experiment, chain, gen, set_type, True)
    W = basics.getWords(experiment, chain, gen, set_type)
    P = prototypes(T, W)
    veridical_x = score(T, W, P, Euclidean)
    adjusted_x = MonteCarlo(T, W, P, Euclidean, iterations, veridical_x) if iterations > 0 else None
    return veridical_x, adjusted_x, P

def prototypes(T, W):
    P = {}
    for i in range(0, len(W)):
        try:
            P[W[i]].append(T[i])
        except KeyError:
            P[W[i]] = [T[i]]
    for p in P.keys():
        P[p] = median(array(P[p]), 0)
    return P

def score(T, W, P, Euclidean=True):
    scores = dict(zip(P.keys(), [[0.0,0.0] for i in range(len(P.keys()))]))
    for t in range(0, len(T)):
        best_dist = 999999
        best_proto = ''
        for p in P.keys():
            dist = distance(P[p], T[t], Euclidean)
            if dist < best_dist:
                best_dist = dist
                best_proto = p
        if best_proto == W[t]:
            scores[best_proto][0] += 1.0
        scores[best_proto][1] += 1.0
    return mean( [scores[x][0]/scores[x][1] for x in scores.keys() if scores[x][1] > 1 and len(scores) > 1] )

def MonteCarlo(T, W, P, Euclidean, iterations, veridical_x):
    scores = []
    for i in xrange(0, iterations):
        shuffle(W)
        scores.append(score(T, W, P, Euclidean))
    expected_x = mean(scores)
    return (veridical_x - expected_x) / (1.0 - expected_x)

def distance(a, b, Euclidean=True):
    if Euclidean == True:
        return sqrt(sum([(a[i]-b[i])**2 for i in range(0, len(a))]))
    return sum([abs(a[i]-b[i]) for i in range(0, len(a))])
