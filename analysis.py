import Levenshtein
import matplotlib.pyplot as plt
import page
import scipy
import datetime
import geometry

chains_1 = ["A", "B", "C", "D"]
chains_2 = ["E", "F", "G", "H"]

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
#   MEASURE LEARNABILITY IN TRAINING: CALCULATE THE MEAN NORMALIZED LEVENSHTEIN
#   DISTANCE FOR A SPECIFIC INDIVIDUAL'S TRAINING RESULTS

def trainingError(condition, chain_code, generation):
    data = load(condition, chain_code, generation, "log")
    total = 0.0
    for i in range(5, 53):
        lev_dist = Levenshtein.distance(data[i][0], data[i][1])
        norm_lev_dist = lev_dist / float(len(max(data[i][0], data[i][1])))
        total += norm_lev_dist
    mean_distance = total / 48
    return mean_distance

#############################################################################
#   COUNT THE NUMBER OF UNIQUE WORDS FOR GIVEN PARTICIPANT

def numberOfUniqueWords(condition, chain_code, generation):
    dynamic_data = load(condition, chain_code, generation, "d")
    stable_data = load(condition, chain_code, generation, "s")
    dynamic_words = [row[0] for row in dynamic_data]
    stable_words = [row[0] for row in stable_data]
    combined_words = dynamic_words + stable_words
    return len(set(dynamic_words)), len(set(stable_words)), len(set(combined_words))

#############################################################################
#   AVERAGE STRING FREQUENCY

def stringFrequency(condition, chain_code, generation):
    dynamic_data = load(condition, chain_code, generation, "d")
    stable_data = load(condition, chain_code, generation, "s")
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
    filename = "Data/" + str(condition) + "/" + chain_code + "/" + str(generation) + set_type
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
