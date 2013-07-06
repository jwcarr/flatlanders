import Levenshtein
import matplotlib.pyplot as plt
import page
import scipy
import datetime
import geometry

chain_codes = ["A", "B", "C", "D"]

#############################################################################
#   MEASURE LEARNABILITY: CALCULATE THE MEAN NORMALIZED LEVENSHTEIN DISTANCE
#   FOR A SPECIFIC INDIVIDUAL'S OUTPUT

def transmissionError(condition, chain_code, generation, n_back=1):
    output_A = load(condition, chain_code, generation, "s")
    output_B = load(condition, chain_code, generation-n_back, "s")
    total = 0.0
    for i in range(0, len(output_A)):
        lev_dist = Levenshtein.distance(output_A[i][0], output_B[i][0])
        norm_lev_dist = lev_dist / float(len(max(output_A[i][0], output_B[i][0])))
        total += norm_lev_dist
    mean_distance = total / float(len(output_A))
    return mean_distance

#############################################################################
#   COUNT THE NUMBER OF UNIQUE WORDS FOR GIVEN PARTICIPANT

def numberOfUniqueWords(condition, chain_code, generation):
    dynamic_data = load(condition, chain_code, generation, "d")
    stable_data = load(condition, chain_code, generation, "s")
    dynamic_words = []
    stable_words = []
    combined_words = []
    for i in range(0,48):
        if dynamic_data[i][0] not in dynamic_words:
            dynamic_words.append(dynamic_data[i][0])
            if dynamic_data[i][0] not in combined_words:
                combined_words.append(dynamic_data[i][0])
        if stable_data[i][0] not in stable_words:
            stable_words.append(stable_data[i][0])
            if stable_data[i][0] not in combined_words:
                combined_words.append(stable_data[i][0])
    print len(dynamic_words)
    print len(stable_words)
    print len(combined_words)

#############################################################################
#   GET TRANSMISSION ERROR RESULTS FOR A WHOLE BUNCH OF CHAINS

def allErrors(condition):
    results = []
    for i in chain_codes:
        scores = []
        for j in range(1, 11):
            score = transmissionError(condition, i, j, 1)
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

def load(condition, chain_code, generation, set_type):
    filename = "Experiment/data/" + str(condition) + "/" + chain_code + "/" + str(generation) + set_type
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
#   CONVERT MATRIX INTO VECTOR

def matrix2vector(matrix):
    vector = []
    for row in matrix:
        for cell in row:
            vector.append(cell)
    return vector

#############################################################################
#   CALCULATE AVERAGE TIME SPENT ON EACH TEST ITEM

def timePerItem(condition, chain_code, generation):
    set_d = load(condition, chain_code, generation, "d")
    timestamp_1 = stringToTimeStamp(set_d[0][4])
    timestamp_50 = stringToTimeStamp(set_d[47][4])
    difference = timestamp_50 - timestamp_1
    time_per_item_set_d = difference.total_seconds() / 94.0
    return time_per_item_set_d

def stringToTimeStamp(string):
    tim = string.split(":")
    timestamp = datetime.timedelta(hours=int(tim[0]), minutes=int(tim[1]), seconds=int(tim[2]))
    return timestamp
