from matplotlib import pyplot as plt, patches
from scipy.spatial import distance
from sklearn.manifold import MDS
from subprocess import call
import numpy as np
import meaning_space as ms
import rater_analysis as ra
import svg_polygons as svg
import voronoi
import geometry

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

# Compute the Voronoi polygons
polys = voronoi.polygons(coordinates)


def plot_all(chain_wide_palette=True, spectrum=[0.2, 0.9], push_factor=5.0, show_prototypes=False):
  for experiment in range(0, len(chain_codes)):
    plot_experiment(experiment+1, chain_wide_palette, spectrum, push_factor, show_prototypes)


def plot_experiment(experiment, chain_wide_palette=True, spectrum=[0.2, 0.9], push_factor=5.0, show_prototypes=False):
  for chain in chain_codes[experiment-1]:
    print 'Chain: ' + chain
    plot_chain(chain, experiment, chain_wide_palette, spectrum, push_factor, show_prototypes)


def plot_chain(chain, experiment=None, chain_wide_palette=True, spectrum=[0.2, 0.9], push_factor=5.0, show_prototypes=False):

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
    plot(chain, generation, experiment, colour_palette, spectrum, push_factor, show_prototypes)


def plot(chain, generation, experiment=None, colour_palette=None, spectrum=[0.2, 0.9], push_factor=0.0, show_prototypes=False):

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

  # Determine the optimum size for the grid of triangle images / grid of legend labels
  # (a square number larger than the number of unique strings)
  for square in [1, 4, 9, 16, 25, 36, 49]:
    if square >= len(word_dict.keys()):
      break
  grid_size = int(np.sqrt(square))

  # Rearrange words so that they'll appear in alphabetical order along rows of the legend
  words = rearrange(word_dict.keys(), grid_size)

  # Plot MDS coordinates and the Voronoi polygons
  for word in words:
    indices = word_dict[word]
    colour, colour_light = colour_palette[word]
    X, Y = coordinates[indices, 0], coordinates[indices, 1]
    plt.scatter(X, Y, c=colour, label=word, marker='o', s=20, linewidth=0, zorder=1)
    for i in indices:
      ax1.add_patch(patches.Polygon(polys[i], facecolor=colour_light, edgecolor='white', linewidth=0.5, zorder=0))
  
  # Set axis style
  plt.xlim(-1, 1)
  plt.ylim(-1, 1)
  plt.xlabel("MDS dimension 1", fontsize=label_font_size, **font)
  plt.ylabel("MDS dimension 2", fontsize=label_font_size, **font)
  plt.xticks(fontsize=axis_font_size, **font)
  plt.yticks(fontsize=axis_font_size, **font)

  # Set up subplot at bottom for legend
  ax2 = plt.subplot2grid((11,2), (8,0), colspan=2)
  plt.axis('off')

  # Produce the legend
  handles, labels = ax1.get_legend_handles_labels()
  ax2.legend(handles, labels, loc='upper center', frameon=False, prop={'family':'Arial', 'size':7}, ncol=grid_size, scatterpoints=1)
  
  # Tighten plot layout
  plt.tight_layout(pad=0.2, h_pad=0.0)

  # Save matplotlib plot as SVG file
  filename = '/Users/jon/Desktop/plots/' + chain + '/' +  str(generation) + '.svg'
  plt.savefig(filename)
  plt.close()

  # Draw the triangle images and splice them into the matplotlib SVG file
  triangle_code = draw_triangles(triangle_dict, colour_palette, show_prototypes, grid_size)
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

  # If there's only one word, just map that word to a grey colour and return, since
  # it won't make sense to arrange the words in colour space.
  if len(words) == 1:
    return {words[0] : ('#B1B0CB', '#D8D8E5')}

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
    hex_colour = convert_to_hex((r, g, b))
    hex_colour_light = convert_to_hex(lighten(r, g, b))
    hex_values.append((hex_colour, hex_colour_light))

  # Return the colour palette
  return dict(zip(words, hex_values))


def draw_triangles(triangles, colour_palette, show_prototypes, grid_size):

  # Alphabetize words so they can be plotted alphabetically
  words = sorted(triangles.keys())

  # Set up a Canvas object and clear it (WHY THE HELL DOES IT NEED TO BE CLEARED!!!)
  canvas = svg.Canvas(540, 360)
  canvas.clear()

  # Determine the size of each triangle cell, giving 5 points of cell spacing
  point_size = (247.7 / grid_size) - 5.0

  # Determine scaling factor by which all triangles will need to be scaled
  scale_factor = point_size / 500.0

  # Determine the radius of the orienting spots and the width of the strokes
  radius = 8.0 * scale_factor
  stroke = max([0.5, 2.0 * scale_factor])

  # Start at cell 0,0
  x_position = 0
  y_position = 0

  # For each of the words...
  for word in words:

    # Determine the offset and colour, and draw the bounding box to the canvas
    offset = np.array([290.0 + (x_position * point_size) + (x_position * 5.0), 6.45 + (y_position * point_size) + (y_position * 5.0)])
    colour, colour_light = colour_palette[word]
    canvas.add_box(offset, point_size, point_size)

    # For each triangle labelled by this word...
    for triangle in triangles[word]:

      # Translate and scale the triangle, and draw it to the canvas
      trans_triangle = (triangle * scale_factor) + offset
      canvas.add_polygon(trans_triangle, border_colour=colour, stroke_width=stroke)
      canvas.add_circle(trans_triangle[0], radius, border_colour=colour, fill_colour=colour)

    # If there's more than one triangle in the set, produce a prototype and draw it to the canvas
    if len(triangles[word]) > 1 and show_prototypes == True:
      prototype = make_prototype(triangles[word], False)
      trans_prototype = (prototype * scale_factor) + offset
      canvas.add_polygon(trans_prototype, border_colour=colour, fill_colour=colour_light, stroke_width=stroke)

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


def make_prototype(triangles, spot_based=True):
  trans_triangles = []
  for t in triangles:

    # Centralize the triangle in the plane
    t = geometry.translate(t, np.array([[250.0, 250.0],[250.0, 250.0],[250.0, 250.0]]))

    # If non-spot-based pototype is requested, swap the vertices around so that vertex 1 is
    # the pointiest one.
    if spot_based == False:
      angles = [geometry.angle(t,1), geometry.angle(t,2), geometry.angle(t,3)]
      min_angle = angles.index(min(angles))
      if min_angle == 0: t = np.array([t[0], t[1], t[2]])
      elif min_angle == 1: t = np.array([t[1], t[2], t[0]])
      elif min_angle == 2: t = np.array([t[2], t[0], t[1]])

    # Rotate the triangle around its centroid so that vertex 1 points North
    t = geometry.rotate(t)

    # Ensure that vertex 2 is to the left of vertex 3 to prevent cancelling out
    if t[1,0] > t[2,0]:
      t = np.array([t[0], t[2], t[1]])

    trans_triangles.append(t)

  # Reformat as Numpy array and take the mean of the coordinates to form the prototype
  trans_triangles = np.asarray(trans_triangles, dtype=float)
  prototype = trans_triangles.mean(axis=0)

  # Shift the prototype such that its bounding box is vertically centralized in the plane
  prototype[:, 1] += ((500.0 - (max([prototype[1,1], prototype[2,1]]) - prototype[0,1])) / 2.0) - prototype[0,1]

  return prototype


# Determine which experiment number a chain belongs to
def determine_experiment_number(chain):
  for experiment in range(0, len(chain_codes)):
    if chain in chain_codes[experiment]:
      break
  return experiment + 1


# Rearrange a list of words so that when displayed in a Matplotlib legend, they will be
# alphabetical along the rows, rather than down the columns.
def rearrange(words, grid_size):
  words = sorted(words)
  words_rearranged = []
  for i in range(grid_size):
    for j in range(grid_size):
      try:
        words_rearranged.append(words[(j*grid_size)+i])
      except IndexError:
        break
  return words_rearranged


# Convert RGB value to hexidecimal triplet
def convert_to_hex(rgb):
  return '#' + "".join(map(chr, [int(round(rgb[0])), int(round(rgb[1])), int(round(rgb[2]))])).encode('hex')


# Lighten a colour by blending in 50% white
def lighten(r, g, b):
  return int(round(r + ((255 - r) * 0.5))), int(round(g + ((255 - g) * 0.5))), int(round(b + ((255 - b) * 0.5)))
