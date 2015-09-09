from random import randrange, shuffle
from collections import defaultdict
import basics

chrs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

def rand_id():
  agent_id = ''
  for i in range(0, 6):
    agent_id += chrs[randrange(0, 62)]
  return agent_id

############################################################
# Generate stimulus sets for naive raters in Task 1 to work on

practice_set_task_1 = [[-1, -2], [-3, -4], [-5, -6], [-7, -7], [-8, -9], [-10, -11]]

def generate_task_1(reps, per_rep, tests):
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
      for k in range(1, len(practice_set_task_1)+1):
        this_set.insert(k, practice_set_task_1[k-1])
      agent_id = rand_id()
      agent_ids.append(agent_id)
      data = ''
      for line in this_set:
        data += str(line[0]) + "\t" + str(line[1]) + "\n"
      f = open("../rating_tasks/static_set_pairs/data/" + agent_id, 'w')
      f.write(data[:-1])
      f.close()
  return agent_ids


############################################################
# Generate stimulus sets for naive raters in Task 2 to work on

practice_set_task_2 = [['86,169;120,216;436,399','144,391;208,137;457,168'], ['86,78;211,107;147,483', '300,72;222,477;113,110'], ['42,319;93,132;46,412', '429,92;312,197;119,197'], ['321,361;415,193;224,237', '321,361;415,193;224,237'], ['213,263;455,213;370,59', '177,372;447,44;475,193'], ['280,308;219,21;355,351', '311,180;66,426;446,166'], ['398,474;21,332;153,380', '398,474;21,332;153,380'], ['50,312;460,337;35,192', '50,312;460,337;35,192'], ['259,12;379,60;30,391', '259,12;379,60;30,391']]

def generate_task_2(reps):
  c = 0
  triangles = all_pairs()
  agent_ids = []
  for i in range(0, reps):
    shuffle(triangles)
    sets = []
    for j in range(0, 7):
      triangle_set = triangles[j*379:(j+1)*379]
      for subset in [triangle_set[0:126], triangle_set[126:252], triangle_set[252:379]]:
        this_set = subset[:]
        for k in range(6, 9):
          this_set.append(practice_set_task_2[k])
        shuffle(this_set)
        if c % 2 == 0:
          this_set.insert(0, ["1", "L"])
        else:
          this_set.insert(0, ["1", "R"])
        c += 1
        for k in range(1, 7):
          this_set.insert(k, practice_set_task_2[k-1])
        agent_id = rand_id()
        agent_ids.append(agent_id)
        data = ''
        for line in this_set:
          data += str(line[0]) + "\t" + str(line[1]) + "\n"
        f = open("../rating_tasks/communicative_error/data/raw_sets/" + agent_id, 'w')
        f.write(data[:-1])
        f.close()
        f = open("../rating_tasks/communicative_error/data/valid_id", 'w')
        f.write('\n'.join(agent_ids))
        f.close()
  return agent_ids

def all_pairs():
  triangle_pairs = []
  for chain in ['I', 'J', 'K', 'L']:
    for gen in range(1,11):
      triangle_pairs += generation_pairs(chain, gen)
  return triangle_pairs

def generation_pairs(chain, generation):
  dynamic_set = basics.load(3, chain, generation, "d")
  static_set = basics.load(3, chain, generation, "s")
  triangle_pairs = []
  for item in dynamic_set+static_set:
    target_triangle = item[1] + ';' + item[2] + ';' + item[3]
    selected_triangle = item[5] + ';' + item[6] + ';' + item[7]
    if target_triangle != selected_triangle:
      triangle_pairs.append([target_triangle, selected_triangle])
  return triangle_pairs
