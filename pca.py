import analysis
import meaning_space as ms
import matplotlib.pyplot as plt
from matplotlib.mlab import PCA
from mpl_toolkits.mplot3d import Axes3D

font = {'fontname':'Arial'}
label_font_size = 10
axis_font_size = 8
cols = [['#01AAE9', '#1B346C', '#F44B1A', '#E5C39E'],
        ['#F6C83C', '#4C5B28', '#DB4472', '#B77F60'],
        ['#CBB345', '#609F80', '#4B574D', '#AF420A']]

static_pca_results = PCA(ms.MakeFeatureMatrix(1, 'A', 0, 's'))
static_principal_components = static_pca_results.Y

def plot(experiment, chain, generation, set_type, components=[1, 2], clusters=False, save=False, animate=False):
  if set_type == 's':
    principal_components = static_principal_components
  else:
    pca_results = PCA(ms.MakeFeatureMatrix(experiment, chain, generation, set_type))
    principal_components = pca_results.Y

  strings = ms.getWords(experiment, chain, generation, set_type)

  word_dict = {}
  for i in range(0, len(strings)):
    if strings[i] in word_dict.keys():
      word_dict[strings[i]].append(principal_components[i])
    else:
      word_dict[strings[i]] = [principal_components[i]]

  else:
    clustered_words = analysis.cluster(strings, clusters)
    word_dict = {}
    for i in range(0, len(clustered_words)):
      cluster_name = 'Cluster ' + str(i+1)
      word_dict[cluster_name] = []
      for j in clustered_words[i]:
        word_dict[cluster_name].append(principal_components[j])

  words = sorted(word_dict.keys())

  if len(components) == 2:
    plt.subplots(figsize=(7.5, 4))
    ax1 = plt.subplot2grid((9,2), (0,0), rowspan=8)
    for i in range(0, len(words)):
      points = [[word_dict[words[i]][j][components[0]-1], word_dict[words[i]][j][components[1]-1]] for j in range(0, len(word_dict[words[i]]))]
      x = [row[0] for row in points]
      y = [row[1] for row in points]
      plt.scatter(x, y, c=cols[experiment-1][i], label=words[i], marker='o', s=40, linewidth=0)

    plt.xlim(-7, 7)
    plt.ylim(-7, 7)
    plt.xlabel("Principal component " + str(components[0]), fontsize=label_font_size, **font)
    plt.ylabel("Principal component " + str(components[1]), fontsize=label_font_size, **font)
    plt.xticks(fontsize=axis_font_size, **font)
    plt.yticks(fontsize=axis_font_size, **font)

    ax2 = plt.subplot2grid((9,2), (8,0), colspan=2)
    plt.axis('off')
    handles, labels = ax1.get_legend_handles_labels()
    ax2.legend(handles, labels, loc='upper center', frameon=False, prop={'family':'Arial', 'size':8}, ncol=7, scatterpoints=1)

    plt.tight_layout(pad=0.2, h_pad=0.0)
    #print "PC1: " + str(results.fracs[0]*100) + "%, PC2: " + str(results.fracs[1]*100) + "%"
    #print "Total: " + str((results.fracs[0] + results.fracs[1]) * 100) + "%"
    if save != False:
      plt.savefig(save, dpi=300)
    else:
      plt.show()

  elif len(components) == 3:
    fig1 = plt.figure()
    ax = Axes3D(fig1)

    for i in range(0, len(words)):
      points = [[word_dict[words[i]][j][components[0]-1], word_dict[words[i]][j][components[1]-1], word_dict[words[i]][j][components[2]-1]] for j in range(0, len(word_dict[words[i]]))]
      x = [row[0] for row in points]
      y = [row[1] for row in points]
      z = [row[2] for row in points]
      ax.scatter(x, y, z, c=cols[experiment-1][i], label=words[i], marker='o', s=40, linewidth=0)

    xAxisLine = ((min(x), max(x)), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.
    yAxisLine = ((0, 0), (min(y), max(y)), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.
    zAxisLine = ((0, 0), (0,0), (min(z), max(z))) # 2 points make the z-axis line at the data extrema along z-axis
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.

    ax.set_xlabel("Principal component " + str(components[0]))
    ax.set_ylabel("Principal component " + str(components[1]))
    ax.set_zlabel("Principal component " + str(components[2]))

    if animate == True:
      for i in xrange(0, 360):
        ax.view_init(elev=10., azim=i)
        padding = ""
        if len(str(i)) == 1:
          padding = "00"
        elif len(str(i)) == 2:
          padding = "0"
        plt.savefig("/Users/jon/Desktop/movie/frame" + padding + str(i) + ".png", dpi=300)
    else:
      plt.show()

  else:
    print('I can only plot 2 or 3 components')

  if clusters == False:
    return words
  else:
    clustered_strings = []
    for word in clustered_words:
      row = []
      for string_num in word:
        if strings[string_num] not in row:
          row.append(strings[string_num])
      clustered_strings.append(row)
    return clustered_strings


def figure(experiment, chain, generation, set_type='s', clusters=False, save="/Users/jon/Desktop/"):
  targets = plot(experiment, chain, generation, set_type, [1, 2], clusters, save + chain+str(generation) + '.svg')
  if clusters == False:
    for i in range(0, len(targets)):
      analysis.triangleGraphic(experiment, chain, generation, [targets[i]], True, True, i, save)
  else:
    for i in range(0, len(targets)):
      print "Cluster " + str(i+1) + ": ", targets[i]
      analysis.triangleGraphic(experiment, chain, generation, targets[i], True, True, i, save)







