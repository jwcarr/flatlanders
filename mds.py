# Author: Nelle Varoquaux <nelle.varoquaux@gmail.com>
# Licence: BSD

# From: http://scikit-learn.org/stable/auto_examples/manifold/plot_mds.html

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA

def MDS(X_true):
  # Center the data
  X_true -= X_true.mean()

  similarities = euclidean_distances(X_true)

  mds = manifold.MDS(n_components=18, max_iter=3000, eps=1e-9, dissimilarity="precomputed", n_jobs=1)
  pos = mds.fit(similarities).embedding_

  # Rescale the data
  pos *= np.sqrt((X_true ** 2).sum()) / np.sqrt((pos ** 2).sum())

  # Rotate the data
  clf = PCA(n_components=2)
  X_true = clf.fit_transform(X_true)

  pos = clf.fit_transform(pos)

  fig = plt.figure(1)
  ax = plt.axes([0., 0., 1., 1.])

  plt.scatter(X_true[:, 0], X_true[:, 1], c='r', s=20)
  plt.scatter(pos[:, 0], pos[:, 1], s=20, c='g')
  plt.legend(('True position', 'MDS'), loc='best')

  similarities = similarities.max() / similarities * 100
  similarities[np.isinf(similarities)] = 0

  # Plot the edges
  start_idx, end_idx = np.where(pos)
  #a sequence of (*line0*, *line1*, *line2*), where:: linen = (x0, y0), (x1, y1), ... (xm, ym)
  segments = [[X_true[i, :], X_true[j, :]] for i in range(len(pos)) for j in range(len(pos))]
  values = np.abs(similarities)
  lc = LineCollection(segments, zorder=0, cmap=plt.cm.hot_r, norm=plt.Normalize(0, values.max()))
  lc.set_array(similarities.flatten())
  lc.set_linewidths(0.5 * np.ones(len(segments)))
  ax.add_collection(lc)

  plt.show()
  return values