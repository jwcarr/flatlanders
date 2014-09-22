from scipy import mean, random, spatial, stats, std

def MT(d1, d2, c=1000):
    x = stats.pearsonr(d1, d2)[0]
    m2 = spatial.distance.squareform(d2, "tomatrix")
    m, s = MC(d1, m2, c)
    return (x-m)/s

def MC(v1, m2, c):
    cor = []
    for i in xrange(0, c):
        m2p = SM(m2)
        v2p = spatial.distance.squareform(m2p, "tovector")
        cor.append(stats.pearsonr(v1, v2p)[0])
    return mean(cor), std(cor)

def SM(m):
    n = len(m)
    mp = [[] for i in xrange(0, n)]    
    o = range(0, n)
    random.shuffle(o)
    for i in xrange(0, n):
        for j in xrange(0, n):
            mp[i].append(m[o[i]][o[j]])
    return mp
