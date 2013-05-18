from subprocess import call

chain_a = [['ei', 'EY'], ['or', 'AOr'], ['ai', 'AY'], ['ae', 'AY'],
           ['au', 'AW'], ['oi', 'OY'], ['o', 'OW'], ['i', 'IY'], ['a', 'AA'],
           ['e', 'EH'], ['u', 'UW'], ['ch', 'C'], ['j', 'J'], ['c', 'k'],
           ['ng', 'N'], ['sh', 'S'], ['th', 'T']]

########################################################################
### Produce vocalizations for words and save m4a files in /Alex

def vocalize(matrix):
    for i in matrix:
        path = "Alex/" + i[0] + ".m4a"
        phon = "\"[[inpt PHON]]" + i[1] + "\""
        call(["say", "-o", path, phon])
    return

########################################################################
### Translate the words into machine readable phonemes

def translate(words, mappings):
    matrix = []
    for word in words:
        phon = word
        for mapping in mappings:
            phon = phon.replace(mapping[0], mapping[1])
            stressed_phon = stress(phon)
        matrix.append([word, phon])
    return matrix

########################################################################
### Insert the primary stress marker before the penultimate vowel

def stress(phon):
    b = len(phon) - 5
    onset = phon[:b]
    coda = phon[b:]
    stressed_word = onset + "1" + coda
    return stressed_word

########################################################################
### Load the words from a set file

def load(condition, chain_code, set_number):
    filename = "../Data/experiment " + condition + "/chain " + chain_code + "/SET" + set_number
    f = open(filename, 'r')
    data = f.read()
    f.close()
    words = data.split("\n")
    return words
