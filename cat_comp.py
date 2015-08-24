# Creates a figure showing the difference between the regular and
# categorical structure measures.

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

axis_font_size = 8
label_font_size = 10
legend_font_size = 7.5

def plot():
  plt.figure(1)
  plt.subplots(figsize=(5.5, 3.0))

  # Plot A: General structure
  mean, variance = (0.0, 0.01)
  x, y = normal_distribution(mean, variance)
  ax1 = plt.subplot2grid((6,2), (0,0), rowspan=5)
  ax1.plot(x, y, label='Distribution of sample correlations', c='#3F3AAB')
  ax1.plot([mean, mean], [0, 4.2], label='Mean of sample correlations', c='#3F3AAB', linestyle=":") # Mean
  ax1.plot([0.5, 0.5], [0.05, 4.2], label="Veridical correlation", linestyle="--", dashes=(5,5), c='#67C200') # Veridical
  ax1.set_yticklabels([])
  plt.xlabel("Correlation coefficient", fontsize=label_font_size)
  plt.ylabel("Frequency", fontsize=label_font_size)
  plt.text(-0.90476, 3.794, "(A)", {'fontsize':8}, fontweight='bold')
  plt.annotate('', xy=(0.0, 2.1), xycoords='data', xytext=(0.5, 2.1), textcoords='data', arrowprops={'arrowstyle': '|-|, widthA=0.5, widthB=0.5'})
  plt.annotate('z = 5', xy=(0.25, 2.2), ha='center', fontsize=7, xycoords='data', xytext=(0, 0), textcoords='offset points')
  configure_axes()

  # Plot B: Compositional structure
  mean, variance = (0.2, 0.01)
  x, y = normal_distribution(mean, variance)
  ax2 = plt.subplot2grid((6,2), (0,1), rowspan=5)
  ax2.plot(x, y, c='#3F3AAB')
  ax2.plot([mean, mean], [0, 4.2], linestyle=":", c='#3F3AAB') # Mean
  ax2.plot([0.5, 0.5], [0.05, 4.2], label="Veridical correlation", linestyle="--", dashes=(5,5), c='#67C200') # Veridical
  ax2.set_yticklabels([])
  plt.xlabel("Correlation coefficient", fontsize=label_font_size)
  plt.text(-0.90476, 3.794, "(B)", {'fontsize':8}, fontweight='bold')
  plt.annotate('', xy=(0.2, 2.1), xycoords='data', xytext=(0.5, 2.1), textcoords='data', arrowprops={'arrowstyle': '|-|, widthA=0.5, widthB=0.5'})
  plt.annotate('z = 3', xy=(0.35, 2.2), ha='center', fontsize=7, xycoords='data', xytext=(0, 0), textcoords='offset points')
  configure_axes()

  # Legend
  ax3 = plt.subplot2grid((6,2), (5,0), colspan=2)
  plt.axis('off')
  handles, labels = ax1.get_legend_handles_labels()
  ax3.legend(handles, labels, loc='upper center', frameon=False, prop={'size':legend_font_size}, ncol=3, numpoints=1)

  plt.tight_layout(pad=0.2, w_pad=1.0, h_pad=0.00)
  plt.savefig("/Users/jon/Documents/PhD/Manuscripts/Flatlanders/figures/structure_methods.eps")
  plt.clf()

def configure_axes():
  plt.xlim(-1, 1)
  plt.ylim(0, 4.2)
  plt.xticks(fontsize=axis_font_size)
  plt.tick_params(axis='y', which='both', left='off', right='off')
  plt.tick_params(axis='x', which='both', top='off', bottom='off')

def normal_distribution(mean, variance):
  sigma = np.sqrt(variance)
  x = np.linspace(-1, 1, 1000)
  y = mlab.normpdf(x, mean, sigma)
  return x, y