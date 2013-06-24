from random import randrange
import language_generator
from math import sqrt

## Global parameters

consonants = ["d", "f", "k", "m", "p", "z"]
vowels = ["a", "i", "o", "u"]

min_syllables = 2
max_syllables = 4
num_of_items = 50

canvas_width = 500
canvas_height = 500
canvas_border = 10

## Create all the set files you need for a given set of conditions and chains
def createAllSetFiles(conditions=["1","2"], chains=["A", "B", "C", "D"]):
    for i in conditions:
        for j in chains:
            create_set(i, j, "d")
            create_set(i, j, "s")
    return

## Create an initial generation 0 set file
def create_set(condition, chain_code, set_type):
    words = language_generator.create_language(consonants, vowels, min_syllables, max_syllables, num_of_items)
    data = ""
    for i in range(0, num_of_items):
        line = words[i] + "\t" + randomTriangle()
        data = data + "\n" + line
    # remove the last linebreak from data
    writeFile(condition, chain_code, set_type, data[1:])
    return

def randomTriangle():
    # Choose coordinates for point A
    x1 = randrange(canvas_border+1, canvas_width-canvas_border+1)
    y1 = randrange(canvas_border+1, canvas_height-canvas_border+1)
    
    # Choose coordinates for point B
    x2 = randrange(canvas_border+1, canvas_width-canvas_border+1)
    y2 = randrange(canvas_border+1, canvas_height-canvas_border+1)

    # Choose coordinates for point C
    x3 = randrange(canvas_border+1, canvas_width-canvas_border+1)
    y3 = randrange(canvas_border+1, canvas_height-canvas_border+1)

    # Return the coordinates delimited by tabs
    return str(x1) + "," + str(y1) + "\t" + str(x2) + "," + str(y2) + "\t" + str(x3) + "," + str(y3)

def distance(xA, yA, xB, yB):
    return sqrt(((xA - xB)**2) + ((yA - yB)**2))

## Write out a file
def writeFile(condition, chain_code, set_type, data):
    file_path = "Experiment/data/" + condition + "/" + chain_code + "/0" + set_type
    f = open(file_path, 'w')
    f.write(data)
    f.close()
    return
