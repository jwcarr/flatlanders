from random import randrange, shuffle

chrs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
practice_set = [[-1, -2], [-3, -4], [-5, -6], [-7, -7], [-8, -9], [-10, -11]]

def rand_id():
    agent_id = ''
    for i in range(0, 6):
        agent_id += chrs[randrange(0, 62)]
    return agent_id

def generate(reps, per_rep, tests):
	full_pair_set = []
	for i in range(0, 47):
		for j in range(i+1, 48):
			full_pair_set.append([i, j])
	agent_ids = []
	for i in range(0, reps):
		shuffle(full_pair_set)
		for j in range(0, per_rep):
			first = (j*(1128/per_rep))
			last = first + (1128/per_rep)
			this_set = full_pair_set[first:last]
			for k in range(0, tests):
				sub_group_len = (1128/per_rep)/tests
				start =sub_group_len*k
				end =sub_group_len*(k+1)
				this_set.insert(randrange(start+k, end+k), [(k+1)*-1, (k+1)*-1])
			if (j+1) % 2 == 0:
				this_set.insert(0, ["1", "L"])
			else:
				this_set.insert(0, ["1", "R"])
			for k in range(1, len(practice_set)+1):
				this_set.insert(k, practice_set[k-1])
			agent_id = rand_id()
			agent_ids.append(agent_id)
			data = ''
			for line in this_set:
				data += str(line[0]) + "\t" + str(line[1]) + "\n"
			f = open("Rater/data/" + agent_id, 'w')
			f.write(data[:-1])
			f.close()
	return agent_ids
