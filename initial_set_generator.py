from random import randrange
import language_generator

## Global parameters

consonants = ["d", "f", "k", "m", "p", "z"]
vowels = ["a", "i", "o", "u"]

min_syllables = 2
max_syllables = 4
num_of_items = 50

canvas_width = 500
canvas_height = 500
canvas_border = 10

#############################################################################
#   Create all the set files you need for a given set of conditions and chains

def createAllSetFiles(conditions=["1","2"], chains=["A", "B", "C", "D"]):
    for i in conditions:
        for j in chains:
            create_set(i, j, "d")
            create_set(i, j, "s")
    return "Done"

#############################################################################
#   Create an initial generation 0 set file

def create_set(condition, chain_code, set_type):
    # Generate the word set
    words = language_generator.create_language(consonants, vowels, min_syllables, max_syllables, num_of_items)
    # Empty data string
    data = ""
    # For each word...
    for i in range(0, num_of_items):
        # ...create a triangle to go with it
        line = words[i] + "\t" + randomTriangle()
        # Put this pairing in the data string
        data = data + "\n" + line
    # Write the data string to the relevent file
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

## Write out a file
def writeFile(condition, chain_code, set_type, data):
    file_path = "Experiment/data/" + condition + "/" + chain_code + "/0" + set_type
    f = open(file_path, 'w')
    f.write(data)
    f.close()
    return
