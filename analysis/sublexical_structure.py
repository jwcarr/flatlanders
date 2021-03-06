from itertools import permutations
from math import factorial
from scipy.spatial.distance import squareform
import numpy as np

def test(strings, meaning_distances, perms):

  # Compute meaning distance residuals
  meaning_residuals = residualize(meaning_distances)

  # Determine category labels
  category_labels = list(set(strings))

  # Get pairwise edit-distances between category labels and format as square
  # distance matrix
  label_distances = squareform(pairwise_string_distances(category_labels))

  # Number of strings and number of possible category permutations
  m = len(strings)
  n = factorial(len(category_labels))

  # Compute the pairwise string indices to avoid doing this repeatedly in the main loop
  string_iterator = [(i, j) for i in range(0, m) for j in range(i+1, m)]

  # Deterministic test - measure every possible category-meaning mapping.
  # This is used where the number of category permutations is less than the
  # number of requested permutations to run; therefore, it's faster and better
  # to run every permutation.
  if n <= perms:

    # Create an empty array to store the covarience for each permutation
    covariences = np.zeros(n, dtype=float)

    # Iterate over an enumeration of all permutations of category labels
    for p, category_labels in enumerate(permutations(category_labels)):

      # Map each string to its index in the permuted category labels
      string_remapping = [category_labels.index(string) for string in strings]

      # Compile the string distances from the pre-computed label_distances matrix
      string_distances = [label_distances[string_remapping[i], string_remapping[j]] for i, j in string_iterator]

      # Store the covarience between meaning distances and string distances
      covariences[p] = (meaning_residuals * residualize(string_distances)).sum()

  # Stochasitc test - randomly sample the space of category-meaning mappings
  else:

    # Create an empty array to store the covariences
    covariences = np.zeros(perms, dtype=float)

    # Compute the veridical covarience and store it in first position
    covariences[0] = (meaning_residuals * residualize(pairwise_string_distances(strings))).sum()

    # For each permutation...
    for p in range(1, perms):

      # Shuffle the order of category labels
      np.random.shuffle(category_labels)

      # Map each string to its index in the permuted category_labels
      string_remapping = [category_labels.index(string) for string in strings]

      # Compile the string distances from the pre-computed label_distances matrix
      string_distances = [label_distances[string_remapping[i], string_remapping[j]] for i, j in string_iterator]

      # Store the covarience between meaning distances and string distances
      covariences[p] = (meaning_residuals * residualize(string_distances)).sum()

  # Return standard score (z-score)
  return (covariences[0] - covariences.mean()) / covariences.std()

# Return the residuals of an array
def residualize(distances):
  distances = np.asarray(distances, dtype=float)
  return distances - distances.mean()

# Take a list of strings and compute the pairwise edit-distances
def pairwise_string_distances(strings):
  distances = []
  for i in range(0, len(strings)):
    for j in range(i+1, len(strings)):
      distances.append(norm_Levenshtein_distance(strings[i], strings[j]))
  return distances

# Calculate the normalized Levenshtein distance between two strings
def norm_Levenshtein_distance(string1, string2):
  if len(string1) > len(string2):
    string1, string2 = string2, string1
  distances = range(len(string1) + 1)
  for index2, char2 in enumerate(string2):
    newDistances = [index2 + 1]
    for index1, char1 in enumerate(string1):
      if char1 == char2:
        newDistances.append(distances[index1])
      else:
        newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
    distances = newDistances
  return float(distances[-1]) / max(len(string1), len(string2))
