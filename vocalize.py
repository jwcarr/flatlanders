from subprocess import call
import os.path

rules = [['ei', 'EY'],['oo','UW'], ['or', 'AOr'], ['ai', 'AY'], ['ae', 'AY'],
         ['au', 'AW'], ['oi', 'OY'], ['iu', 'IWUW'], ['oa', 'OWAA'],
         ['o', 'OW'], ['ia', 'IYAA'], ['ua', 'UWAA'], ['ou', 'OWUW'],
         ['i', 'IY'], ['a', 'AA'],['e', 'EH'], ['u', 'UW'], ['ch', 'C'],
         ['j', 'J'], ['c', 'k'], ['ng', 'N'], ['sh', 'S'], ['th', 'T'],
         ['zz', 'z'], ['pp', 'p'], ['kk','k'],['dd','d']]

########################################################################
### Produce the missing vocalizations for a participant

def produceVocaliaztionsFor(condition, chain_code, generation):
    words = missingWords(condition, chain_code, generation-1)
    n = len(words)
    print("%s missing words" % n)
    if n > 0:
        print("Transforming missing words...")
        matrix = translate(words)
        print("Vocalizing missing words...")
        vocalize(matrix)
    print("Done")
    return

########################################################################
### Produce vocalizations for words and save m4a files using the 'say'
### command. Place in 'temp' folder for checking.

def vocalize(matrix):
    for i in matrix:
        path = "Experiment/temp/" + i[0] + ".m4a"
        phon = "\"[[inpt PHON]]" + i[1] + "\""
        call(["say", "-o", path, phon])
    return

########################################################################
### Translate the words into machine readable phonemes using rules
### described above.

def translate(words):
    matrix = []
    for word in words:
        phon = word
        for mapping in rules:
            phon = phon.replace(mapping[0], mapping[1])
        stressed_phon = stress(phon)
        matrix.append([word, stressed_phon])
    return matrix

########################################################################
### Insert the primary stress marker before the penultimate vowel.
### Tries to figure out where the stress marker should be inserted
### and inserts the number '1' (primary stress) at that point.

def stress(phon):
    b = None
    if len(phon) > 4:
        if phon[-1] not in ["W", "Y", "H", "A"]:
            if phon[-4] not in ["W", "Y", "H", "A"] and phon[-5] not in ["W", "Y", "H", "A"]:
                b = len(phon) - 7
            else:
                b = len(phon) - 6
        else:
            if phon[-3:-2] not in ["W", "Y", "H", "A"]:
                if phon[-4:-3] not in ["W", "Y", "H", "A"]:
                    b = len(phon) - 6
                else:
                    b = len(phon) - 5
            else:
                b = len(phon) - 4
    elif len(phon) == 4:
        if phon[-1] in ["W", "Y", "H", "A"] and phon[1] in ["W", "Y", "H", "A"]:
            b = 0
        elif phon[-2] in ["W", "Y", "H"]:
            b = 1
        elif phon[-1] in ["W", "Y", "H"]:
            b = 2
        else:
            b = 0
    else:
        if phon[-1] in ["W", "Y", "H", "A"]:
            b = 1
        else:
            b = 0
    if b == None:
        stressed_word = phon
    else:
        onset = phon[:b]
        coda = phon[b:]
        stressed_word = onset + "1" + coda
    return stressed_word

########################################################################
### Load a set file

def load(condition, chain_code, set_file):
    filename = "Experiment/data/" + condition + "/" + chain_code + "/" + set_file
    f = open(filename, 'r')
    data = f.read()
    f.close()
    rows = data.split("\n")
    matrix = []
    for row in rows:
        cells = row.split("\t")
        matrix.append(cells)
    return matrix

########################################################################
### Get words from a loaded data matrix

def getWords(condition, chain_code, generation):
    matrix = load(condition, chain_code, generation + "d")
    words = [row[0] for row in matrix]
    return words

########################################################################
### Determine missing words

def missingWords(condition, chain_code, generation):
    words = getWords(str(condition), chain_code, str(generation))
    missing_words = []
    for word in words:
        if os.path.exists("Experiment/vocalizations/" + word + ".m4a") == False:
            missing_words.append(word)
    return missing_words
