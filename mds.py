from matplotlib import pyplot as plt, patches
from scipy.spatial import distance
from sklearn.manifold import MDS
from subprocess import call
import numpy as np
import meaning_space as ms
import rater_analysis as ra
import svg_polygons as svg
import voronoi

# Globals
chain_codes = [["A", "B", "C", "D"], ["E", "F", "G", "H"], ["I", "J", "K", "L"]]
font = {'fontname':'Arial'}
label_font_size = 10
axis_font_size = 8


# Run ratings through MDS to get coordinates in 2-dimensional space
distance_matrix = distance.squareform(ra.distance_array, 'tomatrix')
mds = MDS(dissimilarity="precomputed", n_components=2, max_iter=3000, random_state=100)
coordinates = mds.fit(distance_matrix).embedding_

# Scale each dimension over the interval [-0.9, 0.9] for a tidy plot
for dim in range(0, coordinates.shape[1]):
  minimum = coordinates[:, dim].min()
  difference = coordinates[:, dim].max() - minimum
  coordinates[:, dim] = (((coordinates[:, dim] - minimum) / difference) * 1.8) - 0.9


def plot_all(chain_wide_palette=True, spectrum=[0.2, 0.9], push_factor=5.0):
  for experiment in range(0, len(chain_codes)):
    plot_experiment(experiment+1, chain_wide_palette, spectrum, push_factor)


def plot_experiment(experiment, chain_wide_palette=True, spectrum=[0.2, 0.9], push_factor=5.0):
  for chain in chain_codes[experiment-1]:
    print 'Chain: ' + chain
    plot_chain(chain, experiment, chain_wide_palette, spectrum, push_factor)


def plot_chain(chain, experiment=None, chain_wide_palette=True, spectrum=[0.2, 0.9], push_factor=5.0):

  # Determine experiment number if none is supplied
  if experiment == None:
    experiment = determine_experiment_number(chain)

  # If one palette has been requested, get all strings from entire chain and create a colour palette
  if chain_wide_palette == True:
    all_strings = []
    for generation in range(0, 11):
      all_strings += ms.getWords(experiment, chain, generation, 's')
    colour_palette = generate_colour_palette(all_strings, spectrum, push_factor)
  else:
    colour_palette = None

  # Produce a plot for each generation
  for generation in range(0, 11):
    plot(chain, generation, experiment, colour_palette, spectrum, push_factor)


def plot(chain, generation, experiment=None, colour_palette=None, spectrum=[0.2, 0.9], push_factor=0.0):

  # Determine experiment number if none supplied
  if experiment == None:
    experiment = determine_experiment_number(chain)

  # Get strings and triangles for this generation
  strings = ms.getWords(experiment, chain, generation, 's')
  triangles = ms.getTriangles(experiment, chain, generation, 's')

  # Pick a colour palette if none has been supplied
  if colour_palette == None:
    colour_palette = generate_colour_palette(strings, spectrum, push_factor)

  # Organize strings and triangles into categories
  word_dict = {}
  triangle_dict = {}
  for i in range(0, len(strings)):
    if strings[i] in word_dict.keys():
      word_dict[strings[i]].append(i)
      triangle_dict[strings[i]].append(triangles[i])
    else:
      word_dict[strings[i]] = [i]
      triangle_dict[strings[i]] = [triangles[i]]

  # Set up subplot in top left
  plt.subplots(figsize=(7.5, 4.93))
  ax1 = plt.subplot2grid((11,2), (0,0), rowspan=8)

  # Compute the Voronoi polygons
  polys = voronoi.polygons(coordinates)

  # Plot MDS coordinates and the Voronoi polygons
  for word in sorted(word_dict.keys()):
    indices = word_dict[word]
    color = colour_palette[word]
    X, Y = coordinates[indices, 0], coordinates[indices, 1]
    plt.scatter(X, Y, c=color, label=word, marker='o', s=20, linewidth=0, zorder=1)
    for i in indices:
      ax1.add_patch(patches.Polygon(polys[i], facecolor=color, edgecolor='white', linewidth=0.5, alpha=0.5, zorder=0))
  
  # Set axis style
  plt.xlim(-1, 1)
  plt.ylim(-1, 1)
  plt.xlabel("MDS coordinate 1", fontsize=label_font_size, **font)
  plt.ylabel("MDS coordinate 2", fontsize=label_font_size, **font)
  plt.xticks(fontsize=axis_font_size, **font)
  plt.yticks(fontsize=axis_font_size, **font)

  # Set up subplot at bottom for legend
  ax2 = plt.subplot2grid((11,2), (8,0), colspan=2)
  plt.axis('off')

  # Produce the legend
  handles, labels = ax1.get_legend_handles_labels()
  ax2.legend(handles, labels, loc='upper center', frameon=False, prop={'family':'Arial', 'size':7}, ncol=8, scatterpoints=1)
  
  # Tighten plot layout
  plt.tight_layout(pad=0.2, h_pad=0.0)

  # Save matplotlib plot as SVG file
  filename = '/Users/jon/Desktop/plots/' + chain + '/' +  str(generation) + '.svg'
  plt.savefig(filename)
  plt.close()

  # Draw the triangle images and splice them into the matplotlib SVG file
  triangle_code = draw_triangles(triangle_dict, colour_palette)
  f = open(filename, 'r')
  graph_code = f.read()
  f.close()
  final_code = graph_code.replace('</svg>', triangle_code + '\n\n</svg>')
  f = open(filename, 'w')
  f.write(final_code)
  f.close()

  # Use Inkscape to convert to PDF and then delete the SVG file
  call(["inkscape", filename, "-A", filename[0:-3] + 'pdf'])
  call(["rm", filename])


def generate_colour_palette(strings, spectrum=[0.0, 1.0], push_factor=0.0):

  # Get list of unique strings
  words = list(set(strings))

  # Create distance matrix giving normalized Levenshtein distances between the words
  # Add on the given push factor to prevent colours from being too similar
  string_distances = np.asarray(ms.stringDistances(words), dtype=float) + push_factor
  string_distance_matrix = distance.squareform(string_distances, 'tomatrix')

  # Run distance matrix through MDS to determine the position of each word in 3-dimensional space
  colour_mds = MDS(dissimilarity='precomputed', n_components=3, max_iter=2000, random_state=100)
  colour_coordinates = colour_mds.fit(string_distance_matrix).embedding_

  # Scale the dimensions of the space over the interval [0, 255] to create an RGB colour space.
  # The spectrum argument determines how much of the colour space will be used, allowing you to
  # avoid very dark and very light colours.
  for dim in range(0, colour_coordinates.shape[1]):
    minimum = colour_coordinates[:, dim].min()
    difference = colour_coordinates[:, dim].max() - minimum
    colour_coordinates[:, dim] = (((colour_coordinates[:, dim] - minimum) / difference) * (255 * (spectrum[1] - spectrum[0]))) + (255 * spectrum[0])

  # Convert RGB values to hexadecimal triplets
  hex_values = []
  for r, g, b in colour_coordinates:
    hex_values.append('#' + "".join(map(chr, [int(r), int(g), int(b)])).encode('hex'))

  # Return the colour palette
  return dict(zip(words, hex_values))


def draw_triangles(triangles, colour_palette):

  # Alphabetize words so they can be plotted alphabetically
  words = sorted(triangles.keys())

  # Set up a Canvas object and clear it (WHY THE HELL DOES IT NEED TO BE CLEARED!!!)
  canvas = svg.Canvas(540, 360)
  canvas.clear()

  # Determine the optimum size for the grid of triangle images (a square number larger
  # than the number of unique strings)
  for square in [1, 4, 9, 16, 25, 36, 49]:
    if square >= len(words):
      break

  # Number of rows/columns that will make up the grid
  grid_size = np.sqrt(square)

  # Determine the size of each triangle cell, giving 10 points of cell spacing
  point_size = (247.7 / grid_size) - 5.0

  # Determine scaling factor by which all triangles will need to be scaled
  scale_factor = point_size / 500.0

  # Start at cell 0,0
  x_position = 0
  y_position = 0

  # For each of the words...
  for word in words:

    # Determine the offset and colour, and draw the bounding box to the canvas
    offset = np.array([290.0 + (x_position * point_size) + (x_position * 5.0), 6.45 + (y_position * point_size) + (y_position * 5.0)])
    colour = colour_palette[word]
    canvas.add_box(offset, point_size, point_size)

    # For each triangle labelled by this word...
    for triangle in triangles[word]:

      # Translate and scale the triangle, and draw it to the canvas
      trans_triangle = (triangle * scale_factor) + offset
      canvas.add_polygon(trans_triangle, border_colour=colour)

    # Produce the prototype for this set of triangles and draw it to the canvas

    # Increment the x and y positions
    if x_position < grid_size-1:
      x_position += 1
    else:
      x_position = 0
      y_position += 1

  # Turn the canvas objects into SVG code
  canvas.write_everything()

  # Return the SVG code for the canvas
  return canvas.canvas


def determine_experiment_number(chain):
  for experiment in range(0, len(chain_codes)):
    if chain in chain_codes[experiment]:
      break
  return experiment + 1
