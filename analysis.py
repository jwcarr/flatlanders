import Levenshtein
import matplotlib.pyplot as plt
import page
import scipy
import datetime
import geometry
from random import shuffle

chains_1 = ["A", "B", "C", "D"]
chains_2 = ["E", "F", "G", "H"]

#############################################################################
#   MEASURE LEARNABILITY: CALCULATE THE MEAN NORMALIZED LEVENSHTEIN DISTANCE
#   AND RUN IT THROUGH A MONTE CARLO SIMULATION

def learnability(experiment, chain, generation, simulations=10000):
    words_A = getWords(experiment, chain, generation, "s")
    words_B = getWords(experiment, chain, generation-1, "s")
    x = meanNormLevenshtein(words_A, words_B)
    m, sd = MonteCarloError(words_A, words_B, simulations)
    z = (m-x)/sd
    return x, m, sd, z

def transmissionError(experiment, chain, generation):
    words_A = getWords(experiment, chain, generation, "s")
    words_B = getWords(experiment, chain, generation-1, "s")
    return meanNormLevenshtein(words_A, words_B)

def MonteCarloError(strings1, strings2, simulations):
    distances = []
    for i in xrange(0, simulations):
        shuffle(strings1)
        distances.append(meanNormLevenshtein(strings1, strings2))
    return scipy.mean(distances), scipy.std(distances)

def meanNormLevenshtein(strings1, strings2):
    total = 0.0
    for i in range(0, len(strings1)):
        ld = Levenshtein.distance(strings1[i], strings2[i])
        total += ld/float(max(len(strings1[i]), len(strings2[i])))
    return total/float(len(strings1))

#############################################################################
#   MEASURE LEARNABILITY IN TRAINING: CALCULATE THE MEAN NORMALIZED LEVENSHTEIN
#   DISTANCE FOR A SPECIFIC INDIVIDUAL'S TRAINING RESULTS

def trainingError(experiment, chain, generation, simulations=10000):
    data = load(experiment, chain, generation, "log")
    words_A = [data[x][0] for x in range(5,53)]
    words_B = [data[x][1] for x in range(5,53)]
    x = meanNormLevenshtein(words_A, words_B)
    m, sd = MonteCarloError(words_A, words_B, simulations)
    z = (m-x)/sd
    return x, m, sd, z

#############################################################################
#   COUNT THE NUMBER OF UNIQUE WORDS FOR GIVEN PARTICIPANT

def uniqueStrings(experiment, chain, generation):
    dynamic_data = load(experiment, chain, generation, "d")
    stable_data = load(experiment, chain, generation, "s")
    dynamic_words = [row[0] for row in dynamic_data]
    stable_words = [row[0] for row in stable_data]
    combined_words = dynamic_words + stable_words
    return len(set(dynamic_words)), len(set(stable_words)), len(set(combined_words))

#############################################################################
#   AVERAGE STRING FREQUENCY

def stringFrequency(experiment, chain, generation):
    dynamic_data = load(experiment, chain, generation, "d")
    stable_data = load(experiment, chain, generation, "s")
    dynamic_words = [row[0] for row in dynamic_data]
    stable_words = [row[0] for row in stable_data]
    combined_words = dynamic_words + stable_words
    dynamic_counts = [dynamic_words.count(x) for x in set(dynamic_words)]
    stable_counts = [stable_words.count(x) for x in set(stable_words)]
    combined_counts = [combined_words.count(x) for x in set(combined_words)]
    dynamic_average = sum(dynamic_counts)/float(len(dynamic_counts))
    stable_average = sum(stable_counts)/float(len(stable_counts))
    combined_average = sum(combined_counts)/float(len(combined_counts))
    return dynamic_average, stable_average, combined_average

#############################################################################
#   GET TRANSMISSION ERROR RESULTS FOR A WHOLE BUNCH OF CHAINS

def allTransmissionErrors(experiment):
    results = []
    if experiment == 1:
        chain_codes = chains_1
    else:
        chain_codes = chains_2
    for i in chain_codes:
        scores = []
        for j in range(1, 11):
            score = transmissionError(experiment, i, j, 1)
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
#   GET TRANSMISSION ERROR RESULTS FOR A WHOLE BUNCH OF CHAINS

def allTrainingErrors(experiment):
    results = []
    if experiment == 1:
        chain_codes = chains_1
    else:
        chain_codes = chains_2
    for i in chain_codes:
        scores = []
        for j in range(1, 11):
            score = trainingError(experiment, i, j)
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
#   PLOT MEANS FOR EACH GENERATION WITH ERROR BARS (95% CI)

def plotMean(matrix, start=1, y_label="Score"):
    m = len(matrix)
    n = len(matrix[0])
    means = []
    errors = []
    for i in range(0,n):
        column = [row[i] for row in matrix]
        means.append(scipy.mean(column))
        errors.append((scipy.std(column)/scipy.sqrt(m))*1.96)
    xvals = range(start, n+start)
    plt.errorbar(xvals, means, yerr=errors, fmt='ko', linestyle="-")
    labels = range(start, start+n)
    plt.xticks(xvals, labels)
    plt.xlim(start-0.5, n+start-0.5)
    plt.xlabel("Generation number")
    plt.ylabel(y_label)
    plt.show()

#############################################################################
#   PLOT ALL CHAINS FROM A DATA MATRIX

def plotAll(matrix, start=1, y_label="Score"):
    n = len(matrix[0])
    xvals = range(start, n+start)
    for i in range(0,len(matrix)):
        plt.plot(xvals, matrix[i])
    labels = range(start, start+n)
    plt.xticks(xvals, labels)
    plt.xlim(start, n+start-1)
    plt.xlabel("Generation number")
    plt.ylabel(y_label)
    plt.show()

#############################################################################
#   RUN ALL THREE STATS

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
#   CORRELATE A MATRIX OF RESULTS WITH GENERATION NUMBERS

def pearson(matrix):
    scores = matrix2vector(matrix)
    gen_nums = range(1,len(matrix[0])+1)*len(matrix)
    test = scipy.stats.pearsonr(scores, gen_nums)
    return test[0], len(scores), test[1]/2.0

#############################################################################
#   PAIRED T-TEST BETWEEN FIRST AND LAST GENERATIONS

def student(matrix, hypothesis):
    a = [row[0] for row in matrix]
    b = [row[len(matrix[0])-1] for row in matrix]
    if hypothesis == "ascending" or hypothesis == "a":
        test = scipy.stats.ttest_rel(b, a)
        diff = (float(sum(b))/len(b)) - (float(sum(a))/len(a))
    if hypothesis == "descending" or hypothesis == "d":
        test = scipy.stats.ttest_rel(a, b)
        diff = (float(sum(a))/len(a)) - (float(sum(b))/len(b))
    return diff, len(a)-2, test[0], test[1]/2.0

#############################################################################
#   LOAD RAW DATA FROM A DATA FILE INTO A DATA MATRIX

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
#   LOAD IN THE WORDS FROM A SPECIFIC SET FILE

def getTriangles(experiment, chain, generation, set_type):
    data = load(experiment, chain, generation, set_type)
    triangles = []
    for row in data:
        row[1] = int(row[1].split(',')[0]), int(row[1].split(',')[1])
        row[2] = int(row[2].split(',')[0]), int(row[2].split(',')[1])
        row[3] = int(row[3].split(',')[0]), int(row[3].split(',')[1])
        triangles.append([row[1], row[2], row[3]])
    return triangles

#############################################################################
#   LOAD IN THE WORDS FROM A SPECIFIC SET FILE

def getWords(experiment, chain, generation, set_type):
    data = load(experiment, chain, generation, set_type)
    return [data[x][0] for x in range(0,len(data))]

#############################################################################
#   CONVERT MATRIX INTO VECTOR

def matrix2vector(matrix):
    vector = []
    for row in matrix:
        for cell in row:
            vector.append(cell)
    return vector

#############################################################################
#   CALCULATE AVERAGE TIME SPENT ON EACH TEST ITEM

def timePerItem(experiment, chain, generation):
    set_d = load(experiment, chain, generation, "d")
    timestamp_1 = stringToTimeStamp(set_d[0][4])
    timestamp_50 = stringToTimeStamp(set_d[47][4])
    difference = timestamp_50 - timestamp_1
    time_per_item_set_d = difference.total_seconds() / 94.0
    return time_per_item_set_d

def stringToTimeStamp(string):
    tim = string.split(":")
    timestamp = datetime.timedelta(hours=int(tim[0]), minutes=int(tim[1]), seconds=int(tim[2]))
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
#

def stringDistances(strings):
    distances = []
    for i in range(0,len(strings)):
        for j in range(i+1,len(strings)):
            ld = Levenshtein.distance(strings[i], strings[j])
            distances.append(ld/float(max(len(strings[i]), len(strings[j]))))
    return distances

def meaningDistances(meanings):
    distances = []
    for i in range(0,len(meanings)):
        for j in range(i+1,len(meanings)):
            A = meanings[i]
            B = geometry.translate(A, meanings[j], "centroid")
            distances.append(geometry.triangleDistance(A,B))
    return distances

def distanceCorrelation(distances1, distances2):
    return scipy.stats.pearsonr(distances1, distances2)[0]

def structureScore(experiment, chain, generation, simulations=1000):
    strings = getWords(experiment, chain, generation, "d")
    meanings = getTriangles(experiment, chain, generation, "d")
    string_distances = stringDistances(strings)
    meaning_distances = meaningDistances(meanings)
    x = distanceCorrelation(string_distances, meaning_distances)
    m, sd = MonteCarloStructure(strings, meaning_distances, simulations)
    z = (x-m)/sd
    return x, m, sd, z

def MonteCarloStructure(strings, meaning_distances, simulations):
    correlations = []
    for i in xrange(0, simulations):
        shuffle(strings)
        string_distances = stringDistances(strings)
        correlations.append(distanceCorrelation(meaning_distances, string_distances))
    return scipy.mean(correlations), scipy.std(correlations)
