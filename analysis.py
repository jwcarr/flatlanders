from datetime import timedelta
import geometry
import Levenshtein
import matplotlib.pyplot as plt
import page
from random import shuffle
from scipy import log2, mean, sqrt, stats, std

chains_1 = ["A", "B", "C", "D"]
chains_2 = ["E", "F", "G", "H"]

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
# AVERAGE STRING FREQUENCY

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
# GET STRUCTURE SCORES FOR ALL CHAINS IN AN EXPERIMENT

def allStructureScores(experiment, simulations=1000):
    matrix = []
    if experiment == 1:
        chain_codes = chains_1
    else:
        chain_codes = chains_2
    for i in chain_codes:
        scores = []
        for j in range(0, 11):
            score = structureScore(experiment, i, j, simulations)[3]
            scores.append(score)
        matrix.append(scores)
    return matrix

#############################################################################
# GET TRANSMISSION ERROR RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allTransmissionErrors(experiment):
    results = []
    if experiment == 1:
        chain_codes = chains_1
    else:
        chain_codes = chains_2
    for i in chain_codes:
        scores = []
        for j in range(1, 11):
            score = transmissionError(experiment, i, j)
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
# GET LEARNABILITY RESULTS FOR ALL CHAINS IN AN EXPERIMENT

def allLearnability(experiment):
    results = []
    if experiment == 1:
        chain_codes = chains_1
    else:
        chain_codes = chains_2
    for i in chain_codes:
        scores = []
        for j in range(1, 11):
            score = learnability(experiment, i, j, 100000)[3]
            scores.append(score)
        results.append(scores)
    return results

#############################################################################
# GET TRANSMISSION ERROR RESULTS FOR ALL CHAINS IN AN EXPERIMENT

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
# PLOT MEANS FOR EACH GENERATION WITH ERROR BARS (95% CI)

def plotMean(matrix, start=1, y_label="Score", miny=0.0, maxy=1.0, conf=False):
    m = len(matrix)
    n = len(matrix[0])
    if conf == True:
        plt.plot(range(0,n+2), [1.959964] * (n+2), color='k', linestyle='--')
    means = []
    errors = []    
    for i in range(0,n):
        column = [row[i] for row in matrix if row[i] != None]
        means.append(mean(column))
        errors.append((std(column)/sqrt(m))*1.959964)
    xvals = range(start, n+start)
    plt.errorbar(xvals, means, yerr=errors, color='k', linestyle="-", linewidth=2.0)
    labels = range(start, start+n)
    plt.xticks(xvals, labels)
    plt.xlim(start-0.5, n+start-0.5)
    plt.ylim(miny, maxy)
    plt.xlabel("Generation number", fontsize=18)
    plt.ylabel(y_label, fontsize=18)
    plt.show()

#############################################################################
# PLOT ALL CHAINS FROM A DATA MATRIX

def plotAll(matrix, start=1, y_label="Score", miny=0.0, maxy=1.0, short=True, conf=False):
    if short==True:
        aspect = 0.625
    else:
        aspect = 0.75
    fig, ax = plt.subplots(figsize=plt.figaspect(aspect))
    colours = ["#2E578C","#5D9648","#E7A13D","#BC2D30"]
    n = len(matrix[0])
    xvals = range(start, n+start)
    if conf == True:
        ax.plot(range(0,n+1), [1.959964] * (n+1), color='k', linestyle='--')
    for i in range(0,len(matrix)):
        x_vals = range(start, len(matrix[i])+start)
        ax.plot(x_vals, matrix[i], color=colours[i], linewidth=2.0)
    labels = range(start, start+n)
    plt.xlim(start, n+start-1)
    plt.ylim(miny, maxy) 

    if short==True:
        plt.xticks(xvals, labels, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel("Generation number", fontsize=22)
        plt.ylabel(y_label, fontsize=22)
    else:
        plt.xticks(xvals, labels)
        plt.xlabel("Generation number", fontsize=18)
        plt.ylabel(y_label, fontsize=18)

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
        row[1] = int(row[1].split(',')[0]), int(row[1].split(',')[1])
        row[2] = int(row[2].split(',')[0]), int(row[2].split(',')[1])
        row[3] = int(row[3].split(',')[0]), int(row[3].split(',')[1])
        triangles.append([row[1], row[2], row[3]])
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
# CORRELATE THE STRING EDIT DISTANCES AND MEANING DISTANCES, THEN RUN THE
# DISTANCES THROUGH A MONTE CARLO SIMULATION. RETURN THE VERDICAL COEFFICIENT,
# THE MEAN AND STANDARD DEVIATION OF THE MONTE CARLO SAMPLE, AND THE Z-SCORE

def structureScore(experiment, chain, generation, simulations=1000):
    strings = getWords(experiment, chain, generation, "s")
    meanings = getTriangles(experiment, chain, generation, "s")
    string_distances = stringDistances(strings)
    meaning_distances = meaningDistances(meanings)
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

def meaningDistances(meanings):
    distances = []
    for i in range(0,len(meanings)):
        for j in range(i+1,len(meanings)):
            distances.append(geometry.dT_up_to_rigid_motion(meanings[i],meanings[j]))
    return distances

#############################################################################
# CALCULATE THE ENTROPY OF A LANGUAGE

def entropy(experiment, chain, generation):
    words = getWords(experiment, chain, generation, "c")
    segmented_words = segment(words)
    S = {}
    for word in segmented_words:
        syllables = word.split("|")
        for s in syllables:
            if s in S.keys():
                S[s] += 1.0
            else:
                S[s] = 1.0
    N = float(sum(S.values()))
    H = 0.0 - sum([(s/N)*log2(s/N) for s in S.values()])
    return H

rules = [['ei', 'EY'],['oo','UW'], ['or', 'AOr'], ['ai', 'AY'], ['ae', 'AY'],
         ['au', 'AW'], ['oi', 'OY'], ['iu', 'IWUW'], ['oa', 'OWAA'],
         ['o', 'OW'], ['ia', 'IYAA'], ['ua', 'UWAA'], ['ou', 'OWUW'],
         ['i', 'IY'], ['a', 'AA'],['e', 'EH'], ['u', 'UW'], ['ch', 'C'],
         ['j', 'J'], ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'],
         ['zz', 'z'], ['pp', 'p'], ['kk','k'],['dd','d']]

def segment(words):
    for i in range(0,len(words)):
        for rule in rules:            
            words[i] = words[i].replace(rule[0], rule[1]+"|")
        if words[i][-1] == "|":
            words[i] = words[i][:-1]
    return words

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
