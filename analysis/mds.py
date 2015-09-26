from matplotlib import pyplot as plt, patches
from scipy.spatial import distance
from sklearn.manifold import MDS
import numpy as np
import os
import basics
import rater_analysis
import svg_polygons
import Voronoi
import geometry


# Globals
label_font_size = 10 # points
axis_font_size = 8 # points
legend_font_size = 10 # points
figure_width = 5.5 # inches


def plot_all(chain_wide_palette=True, use_hsb=False, spectrum=[0.2, 0.9], push_factor=5.0, show_prototypes=False, label_cells=False, join_contiguous_cells=False, save_location=False):
  for experiment in range(0, len(basics.chain_codes)):
    plot_experiment(experiment+1, chain_wide_palette, use_hsb, spectrum, push_factor, show_prototypes, label_cells, join_contiguous_cells, save_location)


def plot_experiment(experiment, chain_wide_palette=True, use_hsb=False, spectrum=[0.2, 0.9], push_factor=5.0, show_prototypes=False, label_cells=False, join_contiguous_cells=False, save_location=False):

  # Set directory for saving, and create it if it doesn't exist
  if save_location == False:
    save_location = basics.desktop_location
  save_location += str(experiment) + '/'
  if os.path.exists(save_location) == True:
    if raw_input(save_location + ' already exists. Do you want to overwrite? (y/n) ') != 'y':
      return
  else:
    os.makedirs(save_location)

  for chain in basics.chain_codes[experiment-1]:
    print('Chain: ' + chain)
    plot_chain(chain, experiment, chain_wide_palette, use_hsb, spectrum, push_factor, show_prototypes, label_cells, join_contiguous_cells, save_location)


def plot_chain(chain, experiment=None, chain_wide_palette=True, use_hsb=False, spectrum=[0.2, 0.9], push_factor=5.0, show_prototypes=False, label_cells=False, join_contiguous_cells=False, save_location=False):

  # Determine experiment number if none is supplied
  if experiment == None:
    experiment = basics.determine_experiment_number(chain)

  # If one palette has been requested, get all strings from entire chain and create a colour palette
  if chain_wide_palette == True:
    print('Generating colour palette...')
    all_strings = []
    for generation in range(0, 11):
      all_strings += basics.getWords(experiment, chain, generation, 's')
    colour_palette = generate_colour_palette(all_strings, use_hsb, spectrum, push_factor)
  else:
    colour_palette = None

  # Set directory for saving, and create it if it doesn't exist
  if save_location == False:
    save_location = basics.desktop_location
  save_location += chain + '/'
  if os.path.exists(save_location) == True:
    if raw_input(save_location + ' already exists. Do you want to overwrite? (y/n) ') != 'y':
      return
  else:
    os.makedirs(save_location)

  # Produce a plot for each generation
  print('Generating graphics...')
  for generation in range(0, 11):
    plot(chain, generation, experiment, colour_palette, use_hsb, spectrum, push_factor, show_prototypes, label_cells, join_contiguous_cells, False, save_location, str(generation))


def plot(chain, generation, experiment=None, colour_palette=None, use_hsb=False, spectrum=[0.2, 0.9], push_factor=0.0, show_prototypes=False, label_cells=False, join_contiguous_cells=False, colour_candidates=False, save_location=False, save_name=False):

  # Determine experiment number if none supplied
  if experiment == None:
    experiment = basics.determine_experiment_number(chain)

  # Get strings and triangles for this generation
  strings = basics.getWords(experiment, chain, generation, 's')
  triangles = basics.getTriangles(experiment, chain, generation, 's')

  # Pick a colour palette if none has been supplied
  if colour_palette == None:
    colour_palette = generate_colour_palette(strings, use_hsb, spectrum, push_factor)

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
  plt.subplots(figsize=(figure_width, figure_width/1.375))
  ax1 = plt.subplot2grid((11,2), (0,0), rowspan=7)

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
    X, Y = triangle_coordinates[indices, 0], triangle_coordinates[indices, 1]
    plt.scatter(X, Y, c=colour, label=word, marker='o', s=15, linewidth=0, zorder=1)
    if join_contiguous_cells == True:
      regional_polys = Voronoi.join_contiguous_polygons(voronoi_polygons[indices])
      for poly in regional_polys:
        ax1.add_patch(patches.Polygon(poly, facecolor=colour_light, edgecolor='white', linewidth=0.5, zorder=0))
    else:
      for i in indices:
        ax1.add_patch(patches.Polygon(voronoi_polygons[i], facecolor=colour_light, edgecolor='white', linewidth=0.5, zorder=0))
        if label_cells == True:
          x, y = centroid(voronoi_polygons[i])
          ax1.text(x, y, word, {'fontsize':5}, ha='center', va='center')
  
  # Set axis style
  plt.xlim(-1, 1)
  plt.ylim(-1, 1)
  plt.xlabel("MDS dimension 1", fontsize=label_font_size)
  plt.ylabel("MDS dimension 2", fontsize=label_font_size)
  plt.xticks(fontsize=axis_font_size)
  plt.yticks(fontsize=axis_font_size)

  # Set up subplot at bottom for legend
  ax2 = plt.subplot2grid((11,2), (7,0), colspan=2)
  plt.axis('off')

  # Produce the legend
  handles, labels = ax1.get_legend_handles_labels()
  ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=[0.45, 0.5], frameon=False, prop={'size':legend_font_size}, ncol=grid_size, scatterpoints=1, handletextpad=0.01)
  
  # Tighten plot layout
  plt.tight_layout(pad=0.2, h_pad=0.0)

  # Determine filename and directory if none has been specified
  if type(save_location) == bool and save_location == False:
    save_location = basics.desktop_location
  if type(save_name) == bool and save_name == False:
    save_name = chain + str(generation)
  if colour_candidates != False:
    candidate_num = '_' + str(colour_candidates)
  else:
    candidate_num = ''

  # Save matplotlib plot as SVG file
  filename = save_location + save_name + candidate_num + '.svg'
  plt.savefig(filename)
  plt.close()

  # Draw the triangle images and splice them into the matplotlib SVG file
  triangle_code = draw_triangles(triangle_dict, colour_palette, show_prototypes, grid_size)
  splice_in_triangles(filename, triangle_code)

  # If multiple colour palette candidates have been requested, run plot() again.
  if colour_candidates > 1:
    plot(chain, generation, experiment, None, use_hsb, spectrum, push_factor, show_prototypes, label_cells, join_contiguous_cells, colour_candidates-1, save_location, save_name)


def generate_colour_palette(strings, use_hsb=False, spectrum=[0.0, 1.0], push_factor=0.0):

  # Get list of unique strings
  words = list(set(strings))

  # If there's only one word, just map that word to a grey colour and return, since
  # it won't make sense to arrange the words in colour space.
  if len(words) == 1:
    return {words[0] : ('#B1B0CB', '#D8D8E5')}

  # Create distance matrix giving normalized Levenshtein distances between the words
  # Add on the given push factor to prevent colours from being too similar
  string_distances = np.array(basics.stringDistances(words), dtype=float) + push_factor
  string_distance_matrix = distance.squareform(string_distances, 'tomatrix')

  # Run distance matrix through MDS to determine the position of each word in 3-dimensional space
  string_mds = MDS(dissimilarity='precomputed', n_components=3, n_init=25, max_iter=2000)
  string_coordinates = string_mds.fit_transform(string_distance_matrix)

  hex_colour_values = []

  if use_hsb == True:

    # Scale first dimension in [0, 0.5], which will translate to 0--180 degrees (half of hue space)
    minimum = string_coordinates[:, 0].min()
    difference = string_coordinates[:, 0].max() - minimum
    string_coordinates[:, 0] = ((string_coordinates[:, 0] - minimum) / difference) / 2.0

    # Scale the remaining two dimensions (saturation and brightness) over the specified spectrum
    for dim in range(1, 3):
      minimum = string_coordinates[:, dim].min()
      difference = string_coordinates[:, dim].max() - minimum
      string_coordinates[:, dim] = (((string_coordinates[:, dim] - minimum) / difference) * (spectrum[1] - spectrum[0])) + spectrum[0]

    # Convert HSB values to hexadecimal triplets (the light version is for the Voronoi cells)
    for h, s, b in string_coordinates:
      hex_colour = rgb_to_hex(hsb_to_rgb((h, s, b)))
      hex_colour_light = rgb_to_hex(hsb_to_rgb((h, s, b+0.1)))
      hex_colour_values.append((hex_colour, hex_colour_light))

  else:

    # Scale the dimensions of the space over the interval [0, 255] to create an RGB colour space.
    # The spectrum argument determines how much of the colour space will be used, allowing you to
    # avoid very dark and very light colours.
    for dim in range(0, 3):
      minimum = string_coordinates[:, dim].min()
      difference = string_coordinates[:, dim].max() - minimum
      string_coordinates[:, dim] = (((string_coordinates[:, dim] - minimum) / difference) * (255 * (spectrum[1] - spectrum[0]))) + (255 * spectrum[0])

    # Convert RGB values to hexadecimal triplets (the light version is for the Voronoi cells)
    for r, g, b in string_coordinates:
      hex_colour = rgb_to_hex((r, g, b))
      hex_colour_light = rgb_to_hex(lighten((r, g, b)))
      hex_colour_values.append((hex_colour, hex_colour_light))

  #print('Correspondence: %s' % correspondence_correlation(string_distances, string_coordinates))
  #print('Stress-1: %s' % stress_1(string_mds.stress_, string_distances))

  # Return the colour palette
  return dict(zip(words, hex_colour_values))


def draw_triangles(triangles, colour_palette, show_prototypes, grid_size):

  # Alphabetize words so they can be plotted alphabetically
  words = sorted(triangles.keys())

  # Set up a Canvas object and clear it (WHY THE HELL DOES IT NEED TO BE CLEARED!!!)
  canvas = svg_polygons.Canvas(figure_width*72, (figure_width/1.375)*72)
  canvas.clear()

  # Determine the size of each triangle cell, giving 5 points of cell spacing
  point_size = (171.2 / grid_size) - 5.0

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
    offset = np.array([(figure_width*72*0.575) + (x_position * point_size) + (x_position * 5.0), 6.45 + (y_position * point_size) + (y_position * 5.0)])
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
    t += np.array([250.0, 250.0]) - geometry.centroid(t)

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


# Opens an SVG file and splices in some extra SVG code at the end
def splice_in_triangles(filename, triangle_code):
  f = open(filename, 'r')
  graph_code = f.read()
  f.close()
  final_code = graph_code.replace('</svg>', triangle_code + '\n\n</svg>')
  f = open(filename, 'w')
  f.write(final_code)
  f.close()


# Convert RGB value to hexadecimal triplet
def rgb_to_hex(rgb):
  return '#' + ''.join(map(chr, map(int, map(round, rgb)))).encode('hex')

# Convert hue (radians), saturation [0,1], and brightness [0,1] into RGB
def hsb_to_rgb(hsb):
  if hsb[1] == 0.0: return hsb[2]*255, hsb[2]*255, hsb[2]*255
  h = hsb[0] / (2.0 * np.pi)
  i = int(h*6.)
  f = (h*6.)-i
  p, q, t = hsb[2]*(1.-hsb[1]), hsb[2]*(1.-hsb[1]*f), hsb[2]*(1.-hsb[1]*(1.-f))
  i %= 6
  if i == 0: return hsb[2]*255, t*255, p*255
  elif i == 1: return q*255, hsb[2]*255, p*255
  elif i == 2: return p*255, hsb[2]*255, t*255
  elif i == 3: return p*255, q*255, hsb[2]*255
  elif i == 4: return t*255, p*255, hsb[2]*255
  return hsb[2]*255, p*255, q*255

# Lighten a colour by blending in 50% white
def lighten(rgb):
  return light(rgb[0]), light(rgb[1]), light(rgb[2])
def light(val):
  return int(round(val + ((255 - val) * 0.5)))


# Return the centroid of an arbitrary polygon
# https://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon
def centroid(polygon):
  n = len(polygon)
  a_sum, x_sum, y_sum = 0.0, 0.0, 0.0
  for i in range(0, n):
    if i == n - 1: j = 0
    else: j = i + 1
    p = (polygon[i][0] * polygon[j][1]) - (polygon[j][0] * polygon[i][1])
    a_sum += p
    x_sum += (polygon[i][0] + polygon[j][0]) * p
    y_sum += (polygon[i][1] + polygon[j][1]) * p
  f = 1.0 / (6.0 * (0.5 * a_sum))
  return f * x_sum, f * y_sum


# Calculate the Euclidean distance in n-dimensional space
def ED(a, b):
  return np.sqrt(sum([(a[i]-b[i])**2 for i in range(0, len(a))]))


# Calculate the correspondence correlation - how well do the distances in
# MDS space correlate with the original distances
def correspondence_correlation(distances, mds_coordinates):
  n = len(mds_coordinates)
  mds_distances = [ED(mds_coordinates[i], mds_coordinates[j]) for i in range(n) for j in range(i+1, n)]
  return np.corrcoef(distances, mds_distances)[0,1]


# Calculate stress-1
def stress_1(raw_stress, distances):
  return np.sqrt(raw_stress / sum(distances ** 2))


# Get dissimilarity ratings and format as square distance matrix
triangle_distances = rater_analysis.reliable_distance_array
triangle_distance_matrix = distance.squareform(triangle_distances, 'tomatrix')

# Run ratings through MDS to get coordinates in 2-dimensional space
triangle_mds = MDS(dissimilarity="precomputed", n_components=2, n_init=25, max_iter=2000, random_state=10)
triangle_coordinates = triangle_mds.fit_transform(triangle_distance_matrix)

# Scale each dimension over the interval [-0.9, 0.9] for a tidy plot
for dim in range(0, triangle_coordinates.shape[1]):
  minimum = triangle_coordinates[:, dim].min()
  difference = triangle_coordinates[:, dim].max() - minimum
  triangle_coordinates[:, dim] = (((triangle_coordinates[:, dim] - minimum) / difference) * 1.8) - 0.9

# Compute the Voronoi polygons for these MDS coordinates
voronoi_polygons = Voronoi.polygons(triangle_coordinates, [[-1,-1], [-1,1], [1,1], [1,-1]])

# Print MDS goodness-of-fit stats
#print('Correspondence: %s' % correspondence_correlation(triangle_distances, triangle_coordinates))
#print('Stress-1: %s' % stress_1(triangle_mds.stress_, triangle_distances))
