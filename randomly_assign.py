from random import randrange

chain_codes = ["A", "B", "C", "D"]

# Randomly assign a new participant to a chain and condition

def assignParticipant():
    condition = randrange(1, 3)
    chain = randrange(0, 4)
    chain_code = chain_codes[chain]
    for i in range (0, 10):
        gen = 10 - i
        data = load(condition, chain_code, gen)
        if data == "":
            generation = gen
        else:
            break
    print("Condition %s" % condition)
    print("Chain %s" % chain_code)
    print("Next generation = %s" % generation)

def load(condition, chain_code, generation):
    filename = "Experiment/data/" + str(condition) + "/" + chain_code + "/" + str(generation) + "d"
    f = open(filename, 'r')
    data = f.read()
    f.close()
    return data
