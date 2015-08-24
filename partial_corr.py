# Adapted from https://gist.github.com/fabianp/9396204419c7b638d38f

import numpy as np
from scipy import stats, linalg

def partial_correlation(matrix1, matrix2, control_matrix=False):
  x = np.asarray(matrix1)
  y = np.asarray(matrix2)
  z = np.asarray(control_matrix)
  m = len(matrix1)
  if x.shape[1] > y.shape[1]:
    n = y.shape[1]
    x = np.hstack(x[:, :-1])
    y = np.hstack(y)
  elif x.shape[1] < y.shape[1]:
    n = x.shape[1]
    x = np.hstack(x)
    y = np.hstack(y[:, :-1])
  else:
    n = x.shape[1]
    x = np.hstack(x)
    y = np.hstack(y)
  if type(control_matrix) == bool and control_matrix == False:
    z = np.hstack([np.arange(n, dtype=np.float) for i in range(m)])
  else:
    z = np.hstack([np.asarray(row, dtype=np.float) for row in control_matrix])
  C = np.column_stack([x, y, z])
  return partial_corr(C)

def partial(C):
  n = C.shape[1]
  P_corr = np.zeros((n, n), dtype=np.float)
  P_pval = np.zeros((n, n), dtype=np.float)
  for i in range(n):
    P_corr[i, i] = 1
    P_pval[i, i] = 0
    for j in range(i+1, n):
      idx = np.ones(n, dtype=np.bool)
      idx[i] = False
      idx[j] = False
      beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
      beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]
      res_j = C[:, j] - C[:, idx].dot(beta_i)
      res_i = C[:, i] - C[:, idx].dot(beta_j)
      r, p = stats.pearsonr(res_i, res_j)
      P_corr[i, j] = r
      P_corr[j, i] = r
      P_pval[i, j] = p
      P_pval[j, i] = p
  return P_corr[0,1], P_pval[0,1]