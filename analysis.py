import Levenshtein
import matplotlib.pyplot as plt
import page
import scipy

chain_codes = ["A", "B", "C", "D"]

#############################################################################
#   MEASURE LEARNABILITY: CALCULATE THE MEAN NORMALIZED LEVENSHTEIN DISTANCE
#   FOR A SPECIFIC INDIVIDUAL'S OUTPUT

def transmissionError(chain_code, generation_number, n_back=1):
    if validateTE(chain_code, generation_number, n_back) == False: return
    output_A = getOutput(chain_code, generation_number)
    output_B = getOutput(chain_code, generation_number-n_back)
    total = 0.0
    for i in range(0, len(output_A)):
        lev_dist = Levenshtein.distance(output_A[i], output_B[i])
        norm_lev_dist = lev_dist / float(len(max(output_A[i], output_B[i])))
        total += norm_lev_dist
    mean_distance = total / float(len(output_A))
    return mean_distance

#############################################################################
#   GET TRANSMISSION ERROR RESULTS FOR A WHOLE BUNCH OF CHAINS

def allErrors():
    results = []
    for i in chain_codes:
        scores = []
        for j in range(1, 11):
            score = transmissionError(i, j, 1)
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
#   GET THE OUTPUT DATA FOR A SPECIFIC INDIVIDUAL

def getOutput(chain_code, generation_number):
    raw_data = loadOutput(chain_code, generation_number)
    data_matrix = readOutput(raw_data)
    return data_matrix

#############################################################################
#   LOAD RAW DATA FROM A DATA FILE

def loadOutput(chain_code, generation_number):
    filename = "../Data/Chain " + chain_code + "/" + str(generation_number) + ".txt"
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return data

#############################################################################
#   TAKE RAW DATA AND CONVERT TO A DATA MATRIX

def readOutput(raw_data):
    matrix = []
    lines = raw_data.split("\n")
    for line in lines:
        row = []
        cells = row.split(",")
        for cell in cells:
            row.append(cell)
        matrix.append(row)
    return matrix

#############################################################################
#   VALIDATE TRANSMISSION ERROR PARAMETERS

def validateTE(chain_code, generation_number, n_back):
    if checkChain(chain_code) == False:
        print("Error: Invalid chain"); return False
    if checkGen(generation_number, 1, 10) == False:
        print("Error: Invalid generation number"); return False
    if checkGen(generation_number - n_back, 1, 10) == False:
        print("Error: Invalid n_back value"); return False
    return True

#############################################################################
#   CHECK THAT A GENERATION NUMBER IS VALID

def checkGen(generation_number, lower, upper):
    if generation_number >= lower and generation_number <= upper:
        return True
    else:
        return False

#############################################################################
#   CHECK THAT A CHAIN CODE IS VALID

def checkChain(chain_code):
    if chain_code in chain_codes:
        return True
    else:
        return False

#############################################################################
#   CONVERT MATRIX INTO VECTOR

def matrix2vector(matrix):
    vector = []
    for row in matrix:
        for cell in row:
            vector.append(cell)
    return vector
