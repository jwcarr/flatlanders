'''
A Python implementation of Page's trend test (Page, 1963)
Written by Jon W. Carr

Takes a matrix, with treatments along the columns and replications along
the rows, and returns Page's (1963) L statistic, along with its p-value.

The a-priori hypothesis for directionality must be specified - either
"ascending" or "descending" - depending on the trend that is hypothesized.

Example:

data = [[100,90,105,70,5],
        [200,150,80,50,10],
        [121,130,75,20,25],
        [90,75,76,54,32]]
ptt(data, "descending")

This will return the 4-tuple: (l, m, n, p), where l = Page's L statistic,
m = number of replications, n = number of treatments, and p = the p-value.

Reference:
Page, E. (1963). Ordered hypotheses for multiple treatments: A significance
    test for linear ranks. Journal of the American Statistical Association,
    58, 216-230.
'''

from scipy import stats

critical_values = [[],[],[],[[],[],[28],[41,42],[54,55,56],[66,68,70],[79,81,83],[91,93,96],[104,106,109],[116,119,121],[128,131,134],[141,144,147],[153,156,160],[165,169,172],[178,181,185],[190,194,197],[202,206,210],[215,218,223],[227,231,235],[239,243,248],[251,256,260]],[[],[],[58,60],[84,87,89],[111,114,117],[137,141,145],[163,167,172],[189,193,198],[214,220,225],[240,246,252],[266,272,278],[292,298,305],[317,324,331]],[[],[],[103,106,109],[150,155,160],[197,204,210],[244,251,259],[291,299,307],[338,346,355],[384,393,403],[431,441,451],[477,487,499],[523,534,546],[570,581,593]],[[],[],[166,173,178],[244,252,260],[321,331,341],[397,409,420],[474,486,499],[550,563,577],[625,640,655],[701,717,733],[777,793,811],[852,869,888],[928,946,965]],[[],[],[252,261,269],[370,382,394],[487,501,516],[603,620,637],[719,737,757],[835,855,876],[950,972,994],[1065,1088,1113],[1180,1205,1230],[1295,1321,1348],[1410,1437,1465]],[[],[],[362,376,388],[532,549,567],[701,722,743],[869,893,917],[1037,1063,1090],[1204,1232,1262],[1371,1401,1433],[1537,1569,1603],[1703,1736,1773],[1868,1905,1943],[2035,2072,2112]]]

def ptt(matrix, hypothesis):
    m = len(matrix)
    n = len(matrix[0])
    if n < 3:
        print("Page's trend test requires at least 3 treatments.")
        return
    if m < 2:
        print("Page's trend test requires at least 2 replications.")
        return
    if hypothesis == "ascending" or hypothesis == "a":
        ordered_matrix = mirror_matrix(matrix)
    elif hypothesis == "descending" or hypothesis == "d":
        ordered_matrix = matrix
    else:
        print("Invalid hypothesis. Hypothesis should be set to \"ascending\" or \"descending\".")
        return
    l = page_l(ordered_matrix, m, n)
    if n == 3 and m < 21: p = page_critical_p(l, m, n)
    elif n > 3 and n < 9 and m < 13: p = page_critical_p(l, m, n)
    else: p = page_exact_p(l, m, n, ordered_matrix)
    return l, m, n, p

def page_l(matrix, m, n):
    rank_matrix = []
    for i in range(0,m):
        rank = stats.rankdata(matrix[i])
        rank_list = []
        for j in range(0,n):
            rank_list.append(rank[n-j-1])
        rank_matrix.append(rank_list)
    ranks = []
    for i in range(0,n):
        total = sum([row[i] for row in rank_matrix])
        total = total * (i+1)
        ranks.append(total)
    l = sum(ranks)
    return l

def page_critical_p(l, m, n):
    values = critical_values[n][m]
    level = None
    for i in range(len(values)):
        if l >= values[i]:
            level = i
    if level == 0: return "< 0.05"
    elif level == 1: return "< 0.01"
    elif level == 2: return "< 0.001"
    else: return "= n.s."

def page_exact_p(l, m, n, matrix):
    alt_l = page_l(mirror_matrix(matrix), m, n)
    if alt_l > l:
        return "= n.s."
    else:
        chi_squared = ((12.0*l-3.0*m*n*(n+1.0)**2.0)**2.0)/(m*n**2.0*(n**2.0-1.0)*(n+1.0))
        p_two_tailed = 1 - stats.chi2.cdf(chi_squared, 1)
        p_one_tailed = p_two_tailed / 2.0
    return "= %s" % p_one_tailed

def mirror_matrix(matrix):
    m = len(matrix)
    n = len(matrix[0])
    columns = []
    for i in range(0,n):
        columns.append([row[i] for row in matrix])
    mirrored_matrix = []
    for i in range(0,m):
        new_row = [row[i] for row in columns]
        new_row.reverse()
        mirrored_matrix.append(new_row)
    return mirrored_matrix
