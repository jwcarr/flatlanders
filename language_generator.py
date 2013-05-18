import random

def generate(syllabary, number_of_words=50, min_syllables=4, max_syllables=4):
    words = []
    for i in range(0, number_of_words):
        word = generateWord(syllabary, min_syllables, max_syllables)
        while word in words:
            word = generateWord(syllabary, min_syllables, max_syllables)
        words.append(word)
        print word
    return

def generateWord(syllabary, min_syllables, max_syllables):
    number_of_syllables = random.randrange(min_syllables, max_syllables + 1)
    word = ""
    for i in range(0, number_of_syllables):
        syllable = syllabary[random.randrange(0, len(syllabary))]
        word += syllable
    return word
