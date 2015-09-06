from itertools import permutations
from math import factorial
from scipy.spatial.distance import squareform
import numpy as np
import basics

def test(strings, meaning_distances, perms):

  # Determine category labels and the edit-distances between them
  category_labels = list(set(strings))
  label_distances = squareform(basics.stringDistances(category_labels), force='tomatrix')

  # Compute meaning distance residuals
  meaning_residuals = residualize(meaning_distances)

  # Number of strings, number of categories, and number of category permutations
  m = len(strings)
  n = len(category_labels)
  p = factorial(n)

  # Deterministic test - measure every possible category-meaning mapping
  if p <= perms:
    covariences = np.zeros(p, dtype=float)
    for i, order in enumerate(permutations(range(n))):
      permuted_categories = [category_labels[j] for j in order]
      string_distances = []
      for j in range(0, m):
        idx1 = permuted_categories.index(strings[j])
        for k in range(j+1, m):
          idx2 = permuted_categories.index(strings[k])
          string_distances.append(label_distances[idx1, idx2])
      string_residuals = residualize(string_distances)
      covariences[i] = (meaning_residuals * string_residuals).sum()

  # Stochasitc test - randomly sample the space of category-meaning mappings
  else:
    string_residuals = residualize(basics.stringDistances(strings))
    covariences = np.zeros(perms, dtype=float)
    covariences[0] = (meaning_residuals * string_residuals).sum()
    for i in range(1, perms):
      np.random.shuffle(category_labels)
      string_distances = []
      for j in range(0, m):
        idx1 = category_labels.index(strings[j])
        for k in range(j+1, m):
          idx2 = category_labels.index(strings[k])
          string_distances.append(label_distances[idx1, idx2])
      string_residuals = residualize(string_distances)
      covariences[i] = (meaning_residuals * string_residuals).sum()

  # Return standard score (z-score)
  return (covariences[0] - covariences.mean()) / covariences.std()

def residualize(distances):
  distances = np.array(distances, dtype=float)
  return distances - distances.mean()
