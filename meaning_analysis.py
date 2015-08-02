import meaning_space
import basics

def explore(experiment, chain, generation, chunks, syllable, position):
  strings = basics.getWords(experiment, chain, generation, "s")
  strings = syllablize(strings, chunks)
  triangles = basics.getTriangles(experiment, chain, generation, "s")
  feature_matrix = meaning_space.MakeFeatureMatrix(triangles)
  indices_of_interest = []
  for i in range(0, len(strings)):
    try:
      if syllable in strings[i][position]:
        indices_of_interest.append(i)
    except IndexError:
      continue
  extraction = feature_matrix[indices_of_interest, :]
  for i in range(1, 17):
    mean = extraction[:, i-1].mean()
    z = abs(mean-0.5) / 0.05
    if z > 2:
      print 'Feature %d: %f*' % (i, mean)
    else:
      print 'Feature %d: %f' % (i, mean)

def syllablize(strings, chunks):
  edited_strings = []
  for string in strings:
    edited_string = string
    for chunk in chunks:
      edited_string = edited_string.replace(chunk, '+' + chunk + '+')
    edited_string = edited_string.replace("++", "+")
    if edited_string[0] == '+':
      edited_string = edited_string[1:]
    if edited_string[-1] == "+":
      edited_string = edited_string[0:len(edited_string)-1]
    edited_strings.append(edited_string.split("+"))
  return edited_strings
