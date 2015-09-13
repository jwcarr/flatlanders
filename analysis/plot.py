from math import isinf, isnan
import matplotlib.pyplot as plt
from matplotlib import gridspec
import basics

# Colour palettes adapted from:
#   http://wesandersonpalettes.tumblr.com
#   https://github.com/karthik/wesanderson
#   https://github.com/jiffyclub/palettable

Bottle_Rocket = ["#9B110E", "#3F5151", "#0C1707", "#550307"]
Cavalcanti = ['#D1AA00', '#083213', '#929460', '#6F9879', '#842111']
Chevalier = ['#355243', '#FECA49', '#C9D5D5', '#BBA289']
Darjeeling1 = ["#FF0000", "#F2AD00", "#F98400", "#5BBCD6"]
Darjeeling2 = ["#046C9A", "#D69C4E", "#ECCBAE", "#000000"]
Darjeeling3 = ['#9E9797', '#C28E00', '#836659', '#9C5A33']
Darjeeling4 = ['#D5E3D8', '#618A98', '#F9DA95', '#AE4B16', '#787064']
Fantastic_Fox1 = ["#E2D200", "#46ACC8", "#E58601", "#B40F20"]
Fantastic_Fox2 = ['#F9DB20', '#934B4E', '#42170D', '#C27922', '#E2C8A7']
Fantastic_Fox3 = ['#E4BF44', '#C65742', '#9AD0BB', '#332737', '#ABA18D']
Grand_Budapest1 = ['#EEAE65', '#FB4F55', '#481313', '#CC5F27']
Grand_Budapest2 = ["#E6A0C4", "#C6CDF7", "#D8A499", "#7294D4"]
Grand_Budapest3 = ['#FFA68E', '#FBCCB7', '#8C1108', '#290B04']
Grand_Budapest4 = ['#FFDCB6', '#253845', '#E7AD9D', '#66756E', '#8B3F31', '#966D35']
Life_Aquatic1 = ["#3B9AB2", "#F21A00", "#EBCC2A", "#78B7C5"]
Life_Aquatic2 = ['#0099E6', '#12255A', '#F23814', '#DFB78B', '#B6C3C5']
Life_Aquatic3 = ['#342419', '#1C4027', '#F1C90E', '#665899', '#B89382']
Moonrise1 = ["#F3DF6C", "#CEAB07", "#D5D5D3", "#24281A"]
Moonrise2 = ['#72CADD', '#F0A5B0', '#8C8536', '#C3B477', '#FAD063']
Moonrise3 = ['#667C74', '#B56A27', '#C2BA7C', '#1F1917']
Moonrise4 = ['#7B8761', '#C1A62E', '#4F8F6B', '#3B453C', '#9F3208']
Moonrise5 = ['#DF8C90', '#D8D28E', '#F5BE25', '#3D4A1C', '#D13060', '#A86B4C']
Royal1 = ['#897712', '#F3C2A4', '#F69F97', '#FED68C', '#629075']
Royal2 = ['#768B93', '#BC240F', '#F9ECC5', '#D47329']
Royal3 = ['#87A2A4', '#CAA065', '#D6CABF', '#D6A0A0']
Royal4 = ['#79A43A', '#F2D6AF', '#5E4829', '#181401']
Royal5 = ['#C2ABBA', '#8C3B49', '#B6ACA6', '#212053', '#D1D3D5']
Rushmore = ["#E1BD6D", "#F2300F", "#0B775E", "#35274A"]

# Globals

colours_by_experiment = [Life_Aquatic2, Grand_Budapest1, Darjeeling2]
markers_by_chain = ['s', 'o', 'p', '^']
data_type_ranges = {'expressivity_d':(0,50), 'expressivity_s':(0,50), 'expressivity_c':(0,100), 'structure':(-3,14), 'sublexical_structure':(-3,14), 'transmission_error':(0,1), 'communicative_accuracy':(0,50), 'communicative_error':(25,55), 'sound_symbolism':(-3,7)}
data_type_labels = {'expressivity_d':'Expressivity (dynamic set)', 'expressivity_s':'Expressivity (static set)', 'expressivity_c':'Expressivity', 'structure':'Structure', 'sublexical_structure':'Sublexical structure', 'transmission_error':'Transmission error', 'communicative_accuracy':'Communicative accuracy', 'communicative_error':'Communicative error', 'sound_symbolism':'Sound symbolism'}


class Plot:

  label_font_size = 8.0
  axis_font_size = 7.0
  legend_font_size = 8.0
  line_thickness = 1.0

  def __init__(self, shape_x=1, shape_y=1, width=4.0, height=4.0):
    self.shape_x = int(shape_x)
    self.shape_y = int(shape_y)
    self.height = float(height)
    self.width = float(width)
    self.datasets = [[None] * self.shape_x for y in range(self.shape_y)]
    self.subplots = [[None] * self.shape_x for y in range(self.shape_y)]

  #############################################
  # PUBLIC METHODS

  # Add a subplot to the multipanel plot
  def add(self, dataset, position_x=False, position_y=False):
    if type(dataset) != dict:
      print('Please pass a data dictionary generated from one of the experiment_results() functions.')
      return
    if (type(position_x) == bool and position_x == False) or (type(position_y) == bool and position_y == False):
      position_x, position_y = self.__next_available_position()
      if type(position_x) == bool and position_x == False:
        print('No space left to add a new subplot. Reshape the plot or specify a position to overwrite.')
        return
    else:
      if (position_x > self.shape_x) or (position_y > self.shape_y):
        print('Plot shape is %ix%i. Reshape the plot or specify a different position.' % (self.shape_x, self.shape_y))
        return
      position_x, position_y = position_x-1, position_y-1
    if self.datasets[position_y][position_x] != None and raw_input('Position %i,%i is in use. Overwrite? (y/n) ' % (position_x+1, position_y+1)) != 'y':
      return
    self.datasets[position_y][position_x] = dataset

  # Make the multipanel plot a reality and save as PDF
  def make(self, save_name=False, save_location=False, per_column_legend=False):
    self.fig = plt.figure(figsize=(self.width, self.height))
    legend_height = 0.2 # inches
    if per_column_legend == True:
      legend_height = 0.6
    row_height = (self.height - legend_height) / self.shape_y # inches
    self.grid = gridspec.GridSpec(nrows=self.shape_y+1, ncols=self.shape_x, height_ratios=([row_height] * self.shape_y) + [legend_height])
    subplot_i = 0
    for y in range(self.shape_y):
      one_y_label = False
      if len(set([self.datasets[y][x]['data_type'] for x in range(self.shape_x)])) == 1:
        one_y_label = True
      for x in range(self.shape_x):
        if self.datasets[y][x] == None:
          self.__make_empty_subplot(x, y)
          continue
        self.__make_subplot(x, y, subplot_i, one_y_label)
        subplot_i += 1
    if save_location == False:
      save_location = basics.desktop_location
    if save_name == False:
      save_name = 'plot'
    self.__add_legend(per_column_legend)
    self.grid.tight_layout(self.fig, pad=0.1, h_pad=-.5, w_pad=1)
    plt.savefig(save_location + save_name + '.eps')
    plt.clf()

  # Peek inside the current state of the multipanel plot
  def peek(self):
    print '  ' + ''.join([' %i  '%(x+1) for x in range(self.shape_x)])
    for y in range(self.shape_y):
      print_row = '%i '%(y+1)
      for x in range(self.shape_x):
        if self.datasets[y][x] == None:
          print_row += '[ ] '
        else:
          print_row += '[x] '
      print(print_row)

  def resize(self, width, height):
    self.height = float(height)
    self.width = float(width)

  def reshape(self, shape_x, shape_y):
    shape_x = int(shape_x)
    shape_y = int(shape_y)
    if shape_x > self.shape_x:
      if self.__add_columns(shape_x - self.shape_x) == True:
        self.shape_x = shape_x
    elif shape_x < self.shape_x:
      if self.__remove_columns(self.shape_x - shape_x) == True:
        self.shape_x = shape_x
    if shape_y > self.shape_y:
      if self.__add_rows(shape_y - self.shape_y) == True:
        self.shape_y = shape_y
    elif shape_y < self.shape_y:
      if self.__remove_rows(self.shape_y - shape_y) == True:
        self.shape_y = shape_y

  def set_label_size(self, size):
    self.label_font_size = float(size)

  def set_axis_size(self, size):
    self.axis_font_size = float(size)

  def set_legend_size(self, size):
    self.legend_font_size = float(size)

  def set_line_thickness(self, size):
    self.line_thickness = float(size)

  #############################################
  # PRIVATE METHODS

  def __make_subplot(self, position_x, position_y, subplot_i, one_y_label):
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
    if position_x == 0 or one_y_label == False:
      plt.ylabel(data_type_labels[data_type], fontsize=self.label_font_size)
    if position_x > 0 and one_y_label == True:
      self.subplots[position_y][position_x].set_yticklabels([])
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
    return False, False

  def __add_confidence_intervals(self, min_y, n):
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if min_y < -2:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)

  def __add_chance_level(self, level, n):
    plt.plot(range(-1,n+2), [level] * (n+3), color='gray', linestyle=':', linewidth=0.5)

  def __add_legend(self, per_column_legend):
    if per_column_legend == True:
      for x in range(self.shape_x):
        legend = self.fig.add_subplot(self.grid[self.shape_y, x])
        plt.axis('off')
        legend.set_yticklabels([])
        legend.set_xticklabels([])
        handles, labels = self.subplots[0][x].get_legend_handles_labels()
        plt.legend(handles, labels, loc='lower center', frameon=False, prop={'size':self.legend_font_size}, ncol=2, numpoints=1, handletextpad=0.2)
    else:
      legend = self.fig.add_subplot(self.grid[self.shape_y, :])
      plt.axis('off')
      handles, labels = self.subplots[0][0].get_legend_handles_labels()
      plt.legend(handles, labels, loc='upper center', frameon=False, prop={'size':self.legend_font_size}, ncol=4, numpoints=1)

  def __add_subplot_label(self, subplot_i, min_y, max_y, position):
    try:
      label = '(' + ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[subplot_i]) + ')'
    except IndexError:
      label = '(' + str(subplot_i + 1) + ')'
    padding = abs(min_y - max_y) / 15.
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

  def __add_columns(self, n):
    for y in range(self.shape_y):
      self.datasets[y] += [None] * n
      self.subplots[y] += [None] * n
    return True

  def __remove_columns(self, n):
    cells_in_use = 0
    for row in self.datasets:
      for i in range(1, n+1):
        if row[i*-1] != None:
          cells_in_use += 1
    if cells_in_use > 0:
      plural = ''
      if cells_in_use > 1: plural = 's'
      if raw_input('This will erase %i plot%s. Continue? (y/n) ' % (cells_in_use, plural)) != 'y':
        return False
    for row in self.datasets:
      for i in range(n):
        del row[-1]
    for row in self.subplots:
      for i in range(n):
        del row[-1]
    return True

  def __add_rows(self, n):
    self.datasets += [[None] * self.shape_x for i in range(n)]
    self.subplots += [[None] * self.shape_x for i in range(n)]
    return True

  def __remove_rows(self, n):
    cells_in_use = 0
    for i in range(1, n+1):
      for cell in self.datasets[i*-1]:
        if cell != None:
          cells_in_use += 1
    if cells_in_use > 0:
      plural = ''
      if cells_in_use > 1: plural = 's'
      if raw_input('This will erase %i plot%s. Continue? (y/n) ' % (cells_in_use, plural)) != 'y':
        return False
    for i in range(n):
      del self.datasets[-1]
      del self.subplots[-1]
    return True
