from math import isinf, isnan
import matplotlib.pyplot as plt
from matplotlib import gridspec
import basics


markers_by_chain = ['s', 'o', 'p', '^']
colours_by_experiment = [['#01AAE9', '#1B346C', '#F44B1A', '#E5C39E'], ['#F6C83C', '#4C5B28', '#DB4472', '#B77F60'], ['#CBB345', '#609F80', '#4B574D', '#AF420A']]
data_type_ranges = {'expressivity_d':(0,50), 'expressivity_s':(0,50), 'expressivity_c':(0,100), 'structure':(-3,14), 'sublexical_structure':(-3,14), 'transmission_error':(0,1), 'communicative_accuracy':(0,50), 'communicative_error':(25,55), 'sound_symbolism':(-3,6)}
data_type_labels = {'expressivity_d':'Expressivity (dynamic set)', 'expressivity_s':'Expressivity (static set)', 'expressivity_c':'Expressivity', 'structure':'Structure', 'sublexical_structure':'Sublexical structure', 'transmission_error':'Transmission error', 'communicative_accuracy':'Communicative accuracy', 'communicative_error':'Communicative error', 'sound_symbolism':'Sound symbolism'}


class Plot:

  def __init__(self, shape_x, shape_y, width, height):
  label_font_size = 8.0
  axis_font_size = 7.0
  legend_font_size = 8.0
  line_thickness = 1.0

    self.shape_x = shape_x
    self.shape_y = shape_y
    self.height = height
    self.width = width
    self.n = self.shape_x * self.shape_y
    self.datasets = [[None] * self.shape_x for y in range(self.shape_y)]
    self.subplots = [[None] * self.shape_x for y in range(self.shape_y)]

  def add(self, dataset, position_x=False, position_y=False):
    if position_x == False:
      position_x, position_y = self.next_available_position()
    if (position_x * position_y) > self.n:
      raise ValueError('Insufficient size for this position. Multiplot size is %ix%i' % (self.shape_x, self.shape_y))
    if self.datasets[position_y][position_x] != None and raw_input('Position %i,%i in use. Overwrite? (y/n) ' % (position_x, position_y)) != 'y':
      return
    self.datasets[position_y][position_x] = dataset

  def make(self, save_name=False, save_location=False):
    self.fig = plt.figure(figsize=(self.width, self.height))
    self.grid = gridspec.GridSpec(nrows=self.shape_y+1, ncols=self.shape_x, height_ratios=([0.95 / self.shape_y] * self.shape_y) + [0.05])
    subplot_i = 0
    for y in range(self.shape_y):
      for x in range(self.shape_x):
        if self.datasets[y][x] == None:
          self.__make_empty_subplot(x, y)
          continue
        self.__make_subplot(x, y, subplot_i)
        subplot_i += 1
    if save_location == False:
      save_location = basics.desktop_location
    if save_name == False:
      save_name = 'plot'
    self.__add_legend()
    self.grid.tight_layout(self.fig, pad=0.1, h_pad=-.5, w_pad=1)
    plt.savefig(save_location + save_name + '.eps')
    plt.clf()

  def make_subplot(self, position_x, position_y, subplot_i):
  def set_label_size(self, size):
    self.label_font_size = size

  def set_axis_size(self, size):
    self.axis_font_size = size

  def set_legend_size(self, size):
    self.legend_font_size = size

  def set_line_thickness(self, size):
    self.line_thickness = size

  #############################################
  # PRIVATE METHODS

  def __make_subplot(self, position_x, position_y, subplot_i):
    dataset = self.datasets[position_y][position_x]
    matrix = self.__remove_NaN(dataset['data'])
    experiment = dataset['experiment']
    data_type = dataset['data_type']
    starting_generation = dataset['starting_generation']
    self.subplots[position_y][position_x] = self.fig.add_subplot(self.grid[position_y, position_x])
    colours = colours_by_experiment[experiment-1]
    chain_n = len(matrix)
    generation_n = len(matrix[0])
    if data_type in ['structure', 'sublexical_structure', 'sound_symbolism']:
      self.__add_confidence_intervals(data_type_ranges[data_type][0], generation_n)
    elif (data_type == 'expressivity_d' and experiment == 2) or (data_type == 'communicative_accuracy'):
      self.__add_chance_level(16, generation_n)
    for chain_i in range(0, chain_n):
      x_vals = range(starting_generation, len(matrix[chain_i]) + starting_generation)
      y_vals = [y for y in matrix[chain_i]]
      plt.plot(x_vals, y_vals, color=colours[chain_i], marker=markers_by_chain[chain_i], markersize=5.0, markeredgecolor=colours[chain_i], linewidth=self.line_thickness, label='Chain ' + basics.chain_codes[experiment-1][chain_i])
    plt.xlim(-0.5, generation_n + starting_generation - 0.5)
    plt.ylim(data_type_ranges[data_type][0], data_type_ranges[data_type][1])
    plt.xticks(range(0, 11), range(0, 11), fontsize=self.axis_font_size)
    plt.yticks(fontsize=self.axis_font_size)
    plt.tick_params(axis='x', which='both', bottom='off', top='off')
    plt.ylabel(data_type_labels[data_type], fontsize=self.label_font_size)
    if data_type in ['expressivity_d', 'expressivity_s', 'expressivity_c', 'communicative_accuracy', 'communicative_error', 'transmission_error']:
      self.__add_subplot_label(subplot_i, data_type_ranges[data_type][0], data_type_ranges[data_type][1], 'bottom')
    else:
      self.__add_subplot_label(subplot_i, data_type_ranges[data_type][0], data_type_ranges[data_type][1], 'top')
    if position_y == self.shape_y - 1:
      plt.xlabel('Generation number', fontsize=self.label_font_size)

  def __make_empty_subplot(self, position_x, position_y):
    self.subplots[position_y][position_x] = self.fig.add_subplot(self.grid[position_y, position_x])
    plt.axis('off')

  def __next_available_position(self):
    for y in range(self.shape_y):
      for x in range(self.shape_x):
        if self.datasets[y][x] == None:
          return x, y

  def __add_confidence_intervals(self, min_y, n):
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if min_y < -2:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)

  def __add_chance_level(self, level, n):
    plt.plot(range(-1,n+2), [level] * (n+3), color='gray', linestyle=':', linewidth=0.5)

  def __add_legend(self):
    legend = self.fig.add_subplot(self.grid[self.shape_y, :])
    plt.axis('off')
    handles, labels = self.subplots[0][0].get_legend_handles_labels()
    plt.legend(handles, labels, loc='upper center', frameon=False, prop={'size':self.legend_font_size}, ncol=4, numpoints=1)
    return

  def __add_subplot_label(self, subplot_i, min_y, max_y, position):
    try:
      label = '(' + ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[subplot_i]) + ')'
    except IndexError:
      label = '(' + str(subplot_i + 1) + ')'
    padding = abs(min_y - max_y) / 10.
    if position == 'top':
      plt.text(0.2, max_y - padding, label, {'fontsize':8}, fontweight='bold', ha='left', va='top')
    else:
      plt.text(0.2, min_y + padding, label, {'fontsize':8}, fontweight='bold', ha='left', va='bottom')

  def __remove_NaN(self, matrix):
    new_matrix = []
    for row in matrix:
      new_row = []
      for cell in row:
        if cell != None:
          if isnan(cell) == True:
            new_row.append(None)
          elif isinf(cell) == True:
            new_row.append(None)
          else:
            new_row.append(cell)
      new_matrix.append(new_row)
    return new_matrix
