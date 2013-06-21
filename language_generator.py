import random

def create_language(consonants, vowels, min_syllables=2, max_syllables=4, number_of_words=50):
    syllabary = create_syllabary(consonants, vowels)
    language = generate(syllabary, number_of_words, min_syllables, max_syllables)
    return language

def create_syllabary(consonants, vowels):
    syllables = []
    for i in consonants:
        for j in vowels:
            syllable = i + j
            syllables.append(syllable)
    return syllables

def generate(syllabary, number_of_words, min_syllables, max_syllables):
    words = []
    for i in range(0, number_of_words):
        word = generate_word(syllabary, min_syllables, max_syllables)
        while word in words:
            word = generate_word(syllabary, min_syllables, max_syllables)
        words.append(word)
    return words

def generate_word(syllabary, min_syllables, max_syllables):
    number_of_syllables = random.randrange(min_syllables, max_syllables + 1)
    word = ""
    for i in range(0, number_of_syllables):
        syllable = syllabary[random.randrange(0, len(syllabary))]
        word += syllable
    return word

