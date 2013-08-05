from datetime import timedelta
import geometry
import Levenshtein
import matplotlib.pyplot as plt
import numpy
import page
from random import shuffle, seed
from randomdotorg import RandomDotOrg
from scipy import log, log2, mean, polyfit, sqrt, stats, std
import scipy.cluster

chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"]]

#############################################################################
# MEASURE LEARNABILITY: CALCULATE TRANSMISSION ERROR AND THEN COMPARE THE
# VERIDICAL SCORE TO A MONTE CARLO SAMPLE

def learnability(experiment, chain, generation, simulations=100000):
    words_A = getWords(experiment, chain, generation, "s")
    words_B = getWords(experiment, chain, generation-1, "s")
    x = meanNormLevenshtein(words_A, words_B)
    m, sd = MonteCarloError(words_A, words_B, simulations)
    z = (m-x)/sd
    return x, m, sd, z

# CALCULATE THE TRANSMISSION ERROR BETWEEN TWO CONSECUTIVE PARTICIPANTS

def transmissionError(experiment, chain, generation):
    words_A = getWords(experiment, chain, generation, "s")
    words_B = getWords(experiment, chain, generation-1, "s")
    return meanNormLevenshtein(words_A, words_B)

# GIVEN TWO SETS OF STRINGS, SHUFFLE ONE SET OF STRINGS n TIMES. COMPUTE THE
# MEAN NORMALIZED LEVENSHTEIN DISTANCE FOR EACH SHUFFLING AND RETURN THE MEAN
# AND STANDARD DEVIATION OF THE COMPUTED SCORES

def MonteCarloError(strings1, strings2, simulations):
    distances = []
    for i in xrange(0, simulations):
        shuffle(strings1)
        distances.append(meanNormLevenshtein(strings1, strings2))
    return mean(distances), std(distances)

# CALCULATE THE MEAN NORMALIZED LEVENSHTEIN DISTANCE BETWEEN TWO SETS OF STRINGS

def meanNormLevenshtein(strings1, strings2):
    total = 0.0
    for i in range(0, len(strings1)):
        ld = Levenshtein.distance(strings1[i], strings2[i])
        total += ld/float(max(len(strings1[i]), len(strings2[i])))
    return total/float(len(strings1))

#############################################################################
# MEASURE LEARNABILITY IN TRAINING: CALCULATE THE MEAN NORMALIZED LEVENSHTEIN
# DISTANCE FOR A SPECIFIC INDIVIDUAL'S TRAINING RESULTS

def trainingError(experiment, chain, generation):
    data = load(experiment, chain, generation, "log")
    words_A = [data[x][0] for x in range(5,53)]
    words_B = [data[x][1] for x in range(5,53)]
    x = meanNormLevenshtein(words_A, words_B)
    return x

#############################################################################
# COUNT THE NUMBER OF UNIQUE WORDS FOR GIVEN PARTICIPANT

def uniqueStrings(experiment, chain, generation):
    dynamic_data = load(experiment, chain, generation, "d")
    stable_data = load(experiment, chain, generation, "s")
    dynamic_words = [row[0] for row in dynamic_data]
    stable_words = [row[0] for row in stable_data]
    combined_words = dynamic_words + stable_words
    return len(set(dynamic_words)), len(set(stable_words)), len(set(combined_words))

#############################################################################
# GET TRANSMISSION ERROR RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allTransmissionErrors(experiment):
    results = []
    for chain in chain_codes[experiment-1]:
        scores = []
        for generation in range(1, 11):
            score = transmissionError(experiment, chain, generation)
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
# GET LEARNABILITY RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allLearnability(experiment, sims=100000):
    results = []
    for chain in chain_codes[experiment-1]:
        print "Chain " + chain + "..."
        seed(RandomDotOrg().get_seed())
        scores = []
        for generation in range(1, 11):
            score = learnability(experiment, chain, generation, sims)[3]
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
# GET TRANSMISSION ERROR RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allTrainingErrors(experiment):
    results = []
    for chain in chain_codes[experiment-1]:
        scores = []
        for generation in range(1, 11):
            score = trainingError(experiment, chain, generation)
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
# PLOT MEANS FOR EACH GENERATION WITH ERROR BARS (95% CI)

def plotMean(matrix, start=1, y_label="Score", miny=0.0, maxy=1.0, conf=False):
    fig, ax = plt.subplots(figsize=plt.figaspect(0.625))
    m = len(matrix)
    n = len(matrix[0])
    if conf == True:
        ax.plot(range(0,n+2), [1.959964] * (n+2), color='gray', linestyle=':')
        ax.plot(range(0,n+2), [-1.959964] * (n+2), color='gray', linestyle=':')
        ax.plot(range(0,n+2), [2.734369] * (n+2), color='k', linestyle='--')
        ax.plot(range(0,n+2), [-2.734369] * (n+2), color='k', linestyle='--')
    means = []
    errors = []    
    for i in range(0,n):
        column = [row[i] for row in matrix if row[i] != None]
        means.append(mean(column))
        errors.append((std(column)/sqrt(m))*1.959964)
    xvals = range(start, n+start)
    (_, caps, _) = ax.errorbar(xvals, means, yerr=errors, color='k', linestyle="-", linewidth=2.0, capsize=5.0, elinewidth=1.5)
    for cap in caps:
        cap.set_markeredgewidth(2)
    labels = range(start, start+n)
    plt.xticks(xvals, labels, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlim(start-0.5, n+start-0.5)
    plt.ylim(miny, maxy)
    plt.xlabel("Generation number", fontsize=22)
    plt.ylabel(y_label, fontsize=22)
    plt.show()

#############################################################################
# PLOT ALL CHAINS FROM A DATA MATRIX

def plotAll(matrix, start=1, y_label="Score", miny=0.0, maxy=1.0, conf=False):
    fig, ax = plt.subplots(figsize=plt.figaspect(0.625))
    colours = ["#2E578C","#5D9648","#E7A13D","#BC2D30"]
    n = len(matrix[0])
    xvals = range(start, n+start)
    if conf == True:
        ax.plot(range(0,n+1), [1.959964] * (n+1), color='gray', linestyle=':')
        ax.plot(range(0,n+1), [-1.959964] * (n+1), color='gray', linestyle=':')
        ax.plot(range(0,n+1), [2.734369] * (n+1), color='k', linestyle='--')
        ax.plot(range(0,n+1), [-2.734369] * (n+1), color='k', linestyle='--')
    for i in range(0,len(matrix)):
        x_vals = range(start, len(matrix[i])+start)
        ax.plot(x_vals, matrix[i], color=colours[i], linewidth=2.0)
    labels = range(start, start+n)
    plt.xlim(start, n+start-1)
    plt.ylim(miny, maxy) 
    plt.xticks(xvals, labels, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Generation number", fontsize=22)
    plt.ylabel(y_label, fontsize=22)
    plt.show()

#############################################################################
# RUN ALL THREE STATS

def runStats(matrix, hypothesis="d"):
    page_results = page.ptt(matrix, hypothesis)
    print('''Page's trend test
L = %s, m = %s, n = %s, p %s, one-tailed''' % page_results)
    print("")
    
    pearson_results = pearson(matrix)
    print('''Correlation between scores and generation numbers
r = %s, n = %s, p = %s, one-tailed''' % pearson_results)
    print("")
    
    student_results = student(matrix, hypothesis)
    print('''Paired t-test between first and last generations
diff = %s, t (%s) = %s, p = %s, one-tailed''' % student_results)

#############################################################################
# CORRELATE A MATRIX OF RESULTS WITH GENERATION NUMBERS

def pearson(matrix):
    scores = matrix2vector(matrix)
    gen_nums = range(1,len(matrix[0])+1)*len(matrix)
    test = stats.pearsonr(scores, gen_nums)
    return test[0], len(scores), test[1]/2.0

#############################################################################
# PAIRED T-TEST BETWEEN FIRST AND LAST GENERATIONS

def student(matrix, hypothesis):
    a = [row[0] for row in matrix]
    b = [row[len(matrix[0])-1] for row in matrix]
    if hypothesis == "ascending" or hypothesis == "a":
        test = stats.ttest_rel(b, a)
        diff = (float(sum(b))/len(b)) - (float(sum(a))/len(a))
    if hypothesis == "descending" or hypothesis == "d":
        test = stats.ttest_rel(a, b)
        diff = (float(sum(a))/len(a)) - (float(sum(b))/len(b))
    return diff, len(a)-2, test[0], test[1]/2.0

#############################################################################
# LOAD RAW DATA FROM A DATA FILE INTO A DATA MATRIX

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

#############################################################################
# LOAD IN THE WORDS FROM A SPECIFIC SET FILE

def getTriangles(experiment, chain, generation, set_type):
    if set_type == "c":
        data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
    else:
        data = load(experiment, chain, generation, set_type)
    triangles = []
    for row in data:
        x1, y1 = row[1].split(',')
        x2, y2 = row[2].split(',')
        x3, y3 = row[3].split(',')
        triangles.append(numpy.array([[float(x1),float(y1)],[float(x2),float(y2)],[float(x3),float(y3)]]))
    return triangles

#############################################################################
# LOAD IN THE WORDS FROM A SPECIFIC SET FILE

def getWords(experiment, chain, generation, set_type):
    if set_type == "c":
        data = load(experiment, chain, generation, "d") + load(experiment, chain, generation, "s")
    else:
        data = load(experiment, chain, generation, set_type)
    return [data[x][0] for x in range(0,len(data))]

#############################################################################
# CONVERT MATRIX INTO VECTOR

def matrix2vector(matrix):
    vector = []
    for row in matrix:
        for cell in row:
            vector.append(cell)
    return vector

#############################################################################
# CALCULATE AVERAGE TIME SPENT ON EACH TEST ITEM

def timePerItem(experiment, chain, generation):
    set_d = load(experiment, chain, generation, "d")
    timestamp_1 = stringToTimeStamp(set_d[0][4])
    timestamp_50 = stringToTimeStamp(set_d[47][4])
    difference = timestamp_50 - timestamp_1
    time_per_item_set_d = difference.total_seconds() / 94.0
    return time_per_item_set_d

def stringToTimeStamp(string):
    tim = string.split(":")
    timestamp = timedelta(hours=int(tim[0]), minutes=int(tim[1]), seconds=int(tim[2]))
    return timestamp

#############################################################################
# GET THE OVERUSE COUNT FROM A PARTICIPANT'S LOG FILE (EXP 2 ONLY) I.E. THE
# NUMBER OF TIMES THEY WERE PROMPTED TO ENTER A NEW WORD

def overuseCount(chain, generation):
    data = load(2, chain, generation, "log")
    line = str(data[54])
    split1 = line.split("overuse count = ")
    split2 = split1[1].split("'")
    return int(split2[0])

#############################################################################
# GET STRUCTURE SCORES FOR ALL METRICS

def allMetrics(experiment, sims=1000):
    data = []
    for metric in ['dt','dtt','dtr','dts','dtrm','dtst','dtsr','dtsrm']:
        print "-------------\nMETRIC: " + metric + "\n-------------"
        data.append(allStructureScores(experiment, metric, sims))
    return data

#############################################################################
# GET STRUCTURE SCORES FOR ALL CHAINS IN AN EXPERIMENT

def allStructureScores(experiment, metric='dt', sims=1000):
    meanings = getTriangles(1, "A", 0, "s")
    meaning_distances = meaningDistances(meanings, metric)
    matrix = []
    for chain in chain_codes[experiment-1]:
        print "  Chain " + chain + "..."
        seed(RandomDotOrg().get_seed())
        scores = []
        for generation in range(0, 11):
            if uniqueStrings(experiment, chain, generation)[1] > 3:
                scores.append(structureScore(experiment, chain, generation, metric, sims, meaning_distances)[3])
            else:
                scores.append(None)
        matrix.append(scores)
    return matrix

#############################################################################
# CORRELATE THE STRING EDIT DISTANCES AND MEANING DISTANCES, THEN RUN THE
# DISTANCES THROUGH A MONTE CARLO SIMULATION. RETURN THE VERDICAL COEFFICIENT,
# THE MEAN AND STANDARD DEVIATION OF THE MONTE CARLO SAMPLE, AND THE Z-SCORE

def structureScore(experiment, chain, generation, metric='dt', simulations=1000, meaning_distances=None):
    strings = getWords(experiment, chain, generation, 's')
    string_distances = stringDistances(strings)
    if meaning_distances == None:
        meanings = getTriangles(experiment, chain, generation, 's')
        meaning_distances = meaningDistances(meanings, metric)
    x = stats.pearsonr(string_distances, meaning_distances)[0]
    m, sd = MonteCarloStructure(string_distances, meaning_distances, simulations)
    z = (x-m)/sd
    return x, m, sd, z

# GIVEN STRING EDIT DISTANCES AND MEANING DISTANCES, SHUFFLE THE EDIT DISTANCES
# n TIMES, MEASURING THE CORRELATION BETWEEN EACH. RETURN THE MEAN AND SD OF
# THE CORRELATIONS

def MonteCarloStructure(string_distances, meaning_distances, simulations):
    correlations = []
    for i in xrange(0, simulations):
        shuffle(string_distances)
        correlations.append(stats.pearsonr(meaning_distances, string_distances)[0])
    return mean(correlations), std(correlations)

# FOR EACH PAIR OF STRINGS, CALCULATE THE NORMALIZED LEVENSHTEIN DISTANCE
# BETWEEN THEM

def stringDistances(strings):
    distances = []
    for i in range(0,len(strings)):
        for j in range(i+1,len(strings)):
            ld = Levenshtein.distance(strings[i], strings[j])
            distances.append(ld/float(max(len(strings[i]), len(strings[j]))))
    return distances

# FOR EACH PAIR OF TRIANGLES, CALCULATE THE DISTANCE BETWEEN THEM

def meaningDistances(meanings, metric):
    distances = []
    if metric == "dt":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT(meanings[i],meanings[j]))
    elif metric == "dtt":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_translation(meanings[i],meanings[j]))
    elif metric == "dtr":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_rotation(meanings[i],meanings[j]))
    elif metric == "dts":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_scale(meanings[i],meanings[j]))
    elif metric == "dtrm":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_rigid_motion(meanings[i],meanings[j]))
    elif metric == "dtst":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_scaled_translation(meanings[i],meanings[j]))
    elif metric == "dtsr":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_scaled_rotation(meanings[i],meanings[j]))
    elif metric == "dtsrm":
        for i in range(0,len(meanings)):
            for j in range(i+1,len(meanings)):
                distances.append(geometry.dT_up_to_scaled_rigid_motion(meanings[i],meanings[j]))
    else:
        print "Invalid metric"
        return False
    return distances

#############################################################################
# CALCULATE THE ENTROPY OF A LANGUAGE

def entropy(experiment, chain, generation):
    P = syllableProbabilities(experiment, chain, generation)
    return 0.0-sum([p*log2(p) for p in P])

#############################################################################
# CALCULATE THE CONDITIONAL ENTROPY OF A LANGUAGE

def conditionalEntropy(experiment, chain, generation):
    X, Y, M = bisyllableProbabilities(experiment, chain, generation)
    N = float(len(X))
    return 0.0-sum([M[x][y]*log2(M[x][y]/(X[x]/N)) for x in X.keys() for y in Y.keys()])

#############################################################################
# GET SYLLABLE PROBABILITIES

def syllableProbabilities(experiment, chain, generation):
    words = getWords(experiment, chain, generation, "c")
    segmented_words = segment(words)
    syllables = {}
    for word in segmented_words:
        for syllable in word:
            if syllable in syllables.keys():
                syllables[syllable] += 1.0
            else:
                syllables[syllable] = 1.0
    F = syllables.values()
    N = float(sum(F))
    return [f/N for f in F]

def bisyllableProbabilities(experiment, chain, generation):
    words = getWords(experiment, chain, generation, "c")
    segmented_words = segment(words)
    bisyllables = {}
    for word in segmented_words:
        for i in range(0,len(word)-1):
            bisyll = "|".join(word[i:i+2])
            if bisyll in bisyllables.keys():
                bisyllables[bisyll] += 1.0
            else:
                bisyllables[bisyll] = 1.0
    N = len(bisyllables)
    X = {}
    Y = {}
    for bisyll in bisyllables.keys():
        x, y = bisyll.split("|")
        if x in X.keys():
            X[x] += 1.0
        else:
            X[x] = 1.0
        if y in Y.keys():
            Y[y] += 1.0
        else:
            Y[y] = 1.0
    matrix = {}
    for x in X.keys():
        row = {}
        px = X[x]/float(N)
        for y in Y.keys():
            row[y] = (px*(Y[y]/float(N)))
        matrix[x] = row
    return X, Y, matrix

#############################################################################
# SEGMENT WORDS INTO THEIR COMPONENT SYLLABLES

rules = [['ei', 'EY'],['oo','UW'],['or', 'AOr'],['ai', 'AY'],['ae', 'AY'],
             ['au', 'AW'],['oi', 'OY'],['o', 'OW'],['i', 'IY'],['a', 'AA'],
             ['e', 'EH'],['u', 'UW'],['ch', 'C'],['j', 'J'],['ck', 'k'],
             ['c', 'k'],['ng', 'N'],['sh', 'S'],['th', 'T']]

def segment(words):
    segmented_words = []
    for i in range(0,len(words)):
        for rule in rules:            
            words[i] = words[i].replace(rule[0], rule[1]+"|")
        if words[i][-1] == "|":
            words[i] = words[i][:-1]
        segmented_words.append(words[i].split("|"))
    for i in segmented_words:
        for j in range(0, len(i)):
            if len(i[j]) == 1:
                i[j-1] = i[j-1] + i[j]
                i.pop(j)
                j = j-1
    return segmented_words

#############################################################################
# WRITE OUT A MATRIX TO A FILE ON THE DESKTOP

def writeOut(matrix, filename='file'):
    data = ""
    for row in matrix:
        row = [str(x) for x in row]
        data = data + "\t".join(row) + "\n"
    data = data[0:-1]
    f = open('/Users/jon/Desktop/' + filename + '.txt', 'w')
    f.write(data)
    f.close()

#############################################################################
# READ IN A PREVIOUSLY SAVED DATA FILE TO A MATRIX

def readIn(filename):
    f = open(filename, 'r')
    data = f.read()
    f.close()
    lines = data.split("\n")
    matrix = []
    for line in lines:
        cells = line.split("\t")
        row = []
        for cell in cells:
            try:
                cell = float(cell)
            except:
                cell = None
            row.append(cell)
        matrix.append(row)
    return matrix

#############################################################################
# PLOT A SHAPE-SIZE SCATTER PLOT

def sizeShapePlot(experiment, chain, generation, use_clustering=False, clusters=5):
    triangles = getTriangles(experiment, chain, generation, 's')
    perimeters = [geometry.perimeter(T) for T in triangles]
    areas = [geometry.area(T) for T in triangles]
    words = getWords(experiment, chain, generation, 's')
    uniques = set(words)
    matrix = {}
    for word in uniques:
        dups = []
        for i in range(0, len(words)):
            if words[i] == word:
                dups.append(i)
        matrix[word] = dups
    colours = ["#2E578C","#5D9648","#E7A13D","black","#BC2D30","gray","purple","aqua"]
    i = 0
    fig, ax = plt.subplots(figsize=plt.figaspect(0.75))
    if use_clustering == True:
        clustered_words = cluster(words, clusters)
        L=[]
        for c in clustered_words:
            P = [perimeters[x] for x in c]
            R = [areas[x] for x in c]
            L.append(set([words[x] for x in c]))
            ax.scatter(P, R, color=colours[i], s=40, marker="^")
            i += 1
        clust_labels = []
        print L
        for x in range(1,clusters+1):
            if len(L[x-1]) > 1:
                clust_labels.append("cluster "+str(x))
            else:
                clust_labels.append(str(L[x-1])[6:-3])
        l = plt.legend(clust_labels, loc=2, scatterpoints=1)
    else:        
        for word in matrix.keys():
            P = [perimeters[x] for x in matrix[word]]
            R = [areas[x] for x in matrix[word]]
            ax.scatter(P, R, color=colours[i], s=40, marker="^")
            i += 1    
        l = plt.legend(matrix.keys(), loc=2, scatterpoints=1)
    l.draw_frame(False)
    ax.plot(range(100,1401), [(p**2)/(12*sqrt(3)) for p in range(100,1401)], color='k', linestyle='-')
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel("Perimeter", fontsize=22)
    plt.ylabel("Area (log scale)", fontsize=22)
    plt.xlim(100,1400)
    plt.ylim(100,100000)
    plt.semilogy()
    #plt.savefig(chain+str(generation)+".pdf", transparent=True)
    plt.show()

#############################################################################
# CLUSTER WORDS AND RETURN 

def cluster(words, clusters):
    linkage_matrix = clusterWords(words)
    clustered_words = getClusters(linkage_matrix, clusters, len(words))
    return clustered_words

#############################################################################
# PERFORM AGGLOMERATIVE HIERARCHICAL CLUSTERING AND RETURNS LINKAGE MATRIX

def clusterWords(words):
    distance_matrix = numpy.array([])
    for i in range(0, len(words)):
        for j in range(i + 1, len(words)):
            ld = Levenshtein.distance(words[i], words[j])
            nld = ld/float(max(len(words[i]), len(words[j])))
            distance_matrix = numpy.append(distance_matrix, nld)
    distSquareMatrix = scipy.spatial.distance.squareform(distance_matrix)
    linkage_matrix = scipy.cluster.hierarchy.average(distSquareMatrix)
    return linkage_matrix

#############################################################################
# GET BUILDING BLOCKS GIVEN A LINKAGE MATRIX AND SPECIFIC NUMBER OF BLOCKS

def getClusters(linkage_matrix, clusters, n):
    blocks = [[x] for x in range(0,n)]        
    for i in linkage_matrix:
        if len([value for value in blocks if value != None]) == clusters:
            break
        else:
            merged_block = blocks[int(i[0])] + blocks[int(i[1])]
            blocks.append(merged_block)
            blocks[int(i[0])] = None
            blocks[int(i[1])] = None
    return [value for value in blocks if value != None]

def intergenCorr(x, y, y_axis='ln'):
    m, b = polyfit(x, y, 1)
    ln = [(m*i)+b for i in range(-4,11)]
    fig, ax = plt.subplots(figsize=plt.figaspect(0.625))
    ax.scatter(x, y, marker="x", color='k', s=60)
    ax.plot(range(-4,11), ln, color="#2E578C", linewidth=2.0)
    plt.xlim(-4,10)
    plt.gcf().subplots_adjust(bottom=0.12)
    plt.xlabel("Structure score ($d_{T_{rm}}$) for generation $i-1$", fontsize=22)
    if y_axis == 'ln':
        plt.ylim(-2,8)
        plt.ylabel("Learnability score for generation $i$", fontsize=22)
    else:
        plt.ylim(0,1)
        plt.ylabel("Transmission error for generation $i$", fontsize=22)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.show()

def triangleOverlayGraphic(experiment, chain, generation, word, col, spot_based=True):
    colours = ["#2E578C","#5D9648","#E7A13D","black","#BC2D30","#7D807F","#6F3D79"]
    washed_colours = ["#9AB4D0", "#AED4A7", "#F8D796", "#7F7F7F", "#EA949A", "#C6C8C8", "#C4A2C7"]
    colour = colours[col]
    w_colour = washed_colours[col]
    words = getWords(experiment, chain, generation, "s")
    triangles = getTriangles(experiment, chain, generation, "s")
    html = ""
    T = []
    for i in range(0, len(words)):
        if words[i] in word:

            html = html + "c.beginPath(); c.moveTo("+ str(triangles[i][0][0]) +","+ str(triangles[i][0][1]) +"); c.lineTo("+ str(triangles[i][1][0]) +","+ str(triangles[i][1][1]) +"); c.lineTo("+ str(triangles[i][2][0]) +","+ str(triangles[i][2][1]) +"); c.closePath(); c.lineWidth=3; c.strokeStyle='"+ w_colour +"'; c.stroke(); c.beginPath(); c.arc("+ str(triangles[i][0][0]) +","+ str(triangles[i][0][1]) +", 8, 0, 2 * Math.PI, false); c.fillStyle = '"+ w_colour +"'; c.strokeStyle = '"+ w_colour +"'; c.lineWidth = 1; c.fill(); c.stroke();"

            t = geometry.translate(triangles[i], numpy.array([[240.,240.],[240.,240.],[240.,240.]]))

            if spot_based == True:
                t = geometry.rotate(t)
            else:
                a, b, c = geometry.angle(t,1), geometry.angle(t,2), geometry.angle(t,3)
                angles = {'a':a, 'b':b, 'c':c}
                min_ang = min(angles, key=angles.get)
                if min_ang == 'a':
                    t = numpy.array([[t[0][0], t[0][1]], [t[1][0], t[1][1]], [t[2][0], t[2][1]]])
                elif min_ang == 'b':
                    t = numpy.array([[t[1][0], t[1][1]], [t[2][0], t[2][1]], [t[0][0], t[0][1]]])
                elif min_ang == 'c':
                    t = numpy.array([[t[2][0], t[2][1]], [t[0][0], t[0][1]], [t[1][0], t[1][1]]])
                t = geometry.rotate(t)
            
            if t[1][0] > t[2][0]:
                t = numpy.array([t[0],t[2],t[1]])
            T.append(t)
    N = len(T)
    x1 = sum([T[x][0][0] for x in range(0,N)])/float(N)
    y1 = sum([T[x][0][1] for x in range(0,N)])/float(N)
    x2 = sum([T[x][1][0] for x in range(0,N)])/float(N)
    y2 = sum([T[x][1][1] for x in range(0,N)])/float(N)
    x3 = sum([T[x][2][0] for x in range(0,N)])/float(N)
    y3 = sum([T[x][2][1] for x in range(0,N)])/float(N)
    P = numpy.array([[x1,y1],[x2,y2],[x3,y3]])
    html = html + "c.beginPath(); c.moveTo("+ str(P[0][0]) +","+ str(P[0][1]) +"); c.lineTo("+ str(P[1][0]) +","+ str(P[1][1]) +"); c.lineTo("+ str(P[2][0]) +","+ str(P[2][1]) +"); c.closePath(); c.lineWidth=2; c.strokeStyle='"+ colour +"'; c.fillStyle='"+ colour +"'; c.stroke(); c.fill();"
    writeOutHTML(html, word[0])
    return

def writeOutHTML(html, name):
    data = "<!DOCTYPE HTML>\n<head>\n<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />\n<title>" + name + "</title>\n\n<script type='text/javascript'>function DrawTriangle() { var canvas = document.getElementById('rectangle'); var c = canvas.getContext('2d');" + html + "}</script>       \n</head>\n\n<body onload='DrawTriangle()'>\n\n<table style='width:100%;'>\n    <tr>\n        <td style='text-align:center;'>\n\n        <table style='width:800px; margin-left:auto; margin-right:auto;'>\n            <tr>\n                <td>\n                    <canvas id='rectangle' width='500' height='500' style='border:gray 1px dashed'></canvas>\n                </td>\n            </tr>\n        </table>\n                </td>\n    </tr>\n</table>\n        \n</body>\n        \n</html>"
    f = open('/Users/jon/Desktop/' + name + '.html', 'w')
    f.write(data)
    f.close()
