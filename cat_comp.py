import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

def plot():
  plt.figure(1)
  plt.subplots(figsize=(5.5, 3.0))

  ax1 = plt.subplot2grid((6,2), (0,0), rowspan=5)
  mean = 0
  variance = 0.01
  sigma = np.sqrt(variance)
  x = np.linspace(-3,3,1000)
  y = mlab.normpdf(x,mean,sigma)
  plt.plot(x, y, label='Distribution of sample correlations', c='k')
  plt.plot([mean, mean], [0, 4.2], label='Mean of sample correlations', c='k', linestyle=":") # Mean
  plt.plot([0.5, 0.5], [0.05, 4.2], label="Veridical correlation", linestyle="--", dashes=(5,5), c='#03A7FF') # Veridical
  plt.xlim(-1, 1)
  plt.ylim(0, 4.2)
  plt.xlabel("Correlation coefficient", fontsize=10)
  plt.ylabel("Frequency", fontsize=10)
  plt.xticks(fontsize=8)
  plt.tick_params(axis='y', which='both', left='off', right='off')
  plt.tick_params(axis='x', which='both', top='off', bottom='off')
  ax1.set_yticklabels([])
  text_y = 4.2 - ((4.2/15.)*1.45)
  plt.text(-0.90476, text_y, "(A)", {'fontsize':8}, fontweight='bold')

  ax2 = plt.subplot2grid((6,2), (0,1), rowspan=5)
  mean = 0.2
  variance = 0.01
  sigma = np.sqrt(variance)
  x = np.linspace(-3,3,1000)
  y = mlab.normpdf(x,mean,sigma)
  plt.plot(x, y, c='k')
  plt.plot([mean, mean], [0, 4.2], linestyle=":", c='k') # Mean
  plt.plot([0.5, 0.5], [0.05, 4.2], label="Veridical correlation", linestyle="--", dashes=(5,5), c='#03A7FF') # Veridical
  plt.xlim(-1, 1)
  plt.ylim(0, 4.2)
  plt.xlabel("Correlation coefficient", fontsize=10)
  plt.ylabel("", fontsize=10)
  plt.xticks(fontsize=8)
  plt.tick_params(axis='y', which='both', left='off', right='off')
  plt.tick_params(axis='x', which='both', top='off', bottom='off')
  ax2.set_yticklabels([])
  text_y = 4.2 - ((4.2/15.)*1.45)
  plt.text(-0.90476, text_y, "(B)", {'fontsize':8}, fontweight='bold')

  ax3 = plt.subplot2grid((6,2), (5,0), colspan=2)
  plt.axis('off')
  handles, labels = ax1.get_legend_handles_labels()
  ax3.legend(handles, labels, loc='upper center', frameon=False, prop={'size':7.5}, ncol=3, numpoints=1)

  plt.tight_layout(pad=0.2, w_pad=1.0, h_pad=0.00)
  plt.savefig("/Users/jon/Documents/PhD/Manuscripts/Flatlanders/figures/structure_methods.eps")
  plt.clf()