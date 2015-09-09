from string import ascii_uppercase
from math import isinf, isnan
import matplotlib.pyplot as plt
import numpy as np
import basics


label_font_size = 10
axis_font_size = 8
legend_font_size = 10
line_thickness = 1.0
markers_by_chain = ['s', 'o', 'p', '^']
colours_by_experiment = [['#01AAE9', '#1B346C', '#F44B1A', '#E5C39E'],
                         ['#F6C83C', '#4C5B28', '#DB4472', '#B77F60'],
                         ['#CBB345', '#609F80', '#4B574D', '#AF420A']]


def plot(matrix, mean_line=False, starting_gen=1, miny=0.0, maxy=1.0, y_label="Score", text=False, conf=False, col=1, text_pos='bottom', save=False, matrix_2=False, starting_gen_2=1, miny_2=0.0, maxy_2=1.0, y_label_2="Score", text_2=False, conf_2=False, col_2=1):
  
  # Initialize figure
  plt.figure(1)

  # Replace NaN with None if present in the matrix
  matrix = RemoveNaN(matrix)

  if matrix_2 != False:
    matrix_2 = RemoveNaN(matrix_2)
    if mean_line == True:
      plt.subplots(figsize=(5.5, 2.5))
      ax1 = plt.subplot2grid((6,2), (0,0), rowspan=6)
    else:
      plt.subplots(figsize=(5.5, 3.0))
      ax1 = plt.subplot2grid((6,2), (0,0), rowspan=5)
  else:
    if mean_line == True:
      plt.subplots(figsize=(4.8, 2.5))
      ax1 = plt.subplot2grid((6,1), (0,0), rowspan=6)
    else:
      plt.subplots(figsize=(4.8, 3.0))
      ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5)

  n = len(matrix[0])
  colours = colours_by_experiment[col-1]
  xvals = range(starting_gen, n+starting_gen)
  if conf == True:
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if miny < -2.0:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  elif type(conf) == int:
    plt.plot(range(-1,n+2), [conf] * (n+3), color='gray', linestyle=':', linewidth=0.5)

  if mean_line == True:
    x_vals = range(starting_gen, len(matrix[0])+starting_gen)
    means, errors = MeanWithErrors(matrix)
    _, caps, _ = ax1.errorbar(x_vals, means, yerr=errors, color='k', marker='o', markersize=3.0, linestyle="-", linewidth=line_thickness, capsize=1, elinewidth=0.5)
    for cap in caps:
      cap.set_markeredgewidth(0.5)
  else:
    for i in range(0,len(matrix)):
      x_vals = range(starting_gen, len(matrix[i])+starting_gen)
      y_vals = [item for item in matrix[i]]
      plt.plot(x_vals, y_vals, color=colours[i], marker=markers_by_chain[i], markersize=5.0, markeredgecolor=colours[i], linewidth=line_thickness, label='Chain ' + ascii_uppercase[((col-1)*4)+i:((col-1)*4)+i+1])

  labels = range(starting_gen, starting_gen+n)
  plt.xlim(starting_gen-0.5, n+starting_gen-0.5)
  plt.ylim(miny, maxy)
  plt.xticks(xvals, labels, fontsize=axis_font_size)
  plt.yticks(fontsize=axis_font_size)
  plt.xlabel("Generation number", fontsize=label_font_size)
  plt.ylabel(y_label, fontsize=label_font_size)
  plt.tick_params(axis='x', which='both', bottom='off', top='off')
  if text != False:
    if text_pos == 'bottom':
      text_y = miny + (abs(miny-maxy)/15.)
    else:
      text_y = maxy - ((abs(miny-maxy)/15.)*1.45)
    plt.text(starting_gen, text_y, text, {'fontsize':8}, fontweight='bold')
  
  if matrix_2 != False:
    if mean_line == True:
      ax2 = plt.subplot2grid((6,2), (0,1), rowspan=6)
    else:
      ax2 = plt.subplot2grid((6,2), (0,1), rowspan=5)
    n = len(matrix_2[0])
    colours = colours_by_experiment[col_2-1]
    xvals = range(starting_gen_2, n+starting_gen_2)
    if conf_2 == True:
      plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
      if miny_2 < -2.0:
        plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    elif type(conf_2) == int:
      plt.plot(range(-1,n+2), [conf_2] * (n+3), color='gray', linestyle=':', linewidth=0.5)

    if mean_line == True:
      x_vals = range(starting_gen_2, len(matrix_2[0])+starting_gen_2)
      means, errors = MeanWithErrors(matrix_2)
      _, caps, _ = ax2.errorbar(x_vals, means, yerr=errors, marker='o', markersize=3.0, color='k', linestyle="-", linewidth=line_thickness, capsize=1, elinewidth=0.5)
      for cap in caps:
        cap.set_markeredgewidth(0.5)
    else:
      for i in range(0,len(matrix_2)):
        x_vals = range(starting_gen_2, len(matrix_2[i])+starting_gen_2)
        y_vals = [item for item in matrix_2[i]]
        plt.plot(x_vals, y_vals, color=colours[i], marker=markers_by_chain[i], markersize=5.0, markeredgecolor=colours[i], linewidth=line_thickness)

    labels = range(starting_gen_2, starting_gen_2+n)
    plt.xlim(starting_gen_2-0.5, n+starting_gen_2-0.5)
    plt.ylim(miny_2, maxy_2)
    plt.xticks(xvals, labels, fontsize=axis_font_size)
    plt.yticks(fontsize=axis_font_size)
    plt.xlabel("Generation number", fontsize=label_font_size)
    if y_label_2 != False:
      plt.ylabel(y_label_2, fontsize=label_font_size)
    if (miny == miny_2) and (maxy == maxy_2):
      ax2.set_yticklabels([])
    plt.tick_params(axis='x', which='both', bottom='off', top='off')
    if text_2 != False:
      if text_pos == 'bottom':
        text_y = miny_2 + (abs(miny_2-maxy_2)/15.)
      else:
        text_y = maxy_2 - ((abs(miny_2-maxy_2)/15.)*1.45)
      plt.text(starting_gen_2, text_y, text_2, {'fontsize':8}, fontweight='bold')

  if mean_line == False:
    if matrix_2 != False:
      ax3 = plt.subplot2grid((6,2), (5,0), colspan=2)
    else:
      ax3 = plt.subplot2grid((6,1), (5,0))
    plt.axis('off')
    handles, labels = ax1.get_legend_handles_labels()
    ax3.legend(handles, labels, loc='upper center', frameon=False, prop={'size':legend_font_size}, ncol=4, numpoints=1)

  plt.tight_layout(pad=0.2, w_pad=1.0, h_pad=0.00)

  plt.savefig(save)
  plt.clf()


def chains(dataset, starting_gen=False, miny=False, maxy=False, y_label=False, text=False, conf=False, experiment=False, text_pos=False, save_location=False, save_name=False, dataset2=False, starting_gen2=False, miny2=False, maxy2=False, y_label2=False, text2=False, conf2=False, experiment2=False):
  
  if starting_gen == False:
    if len(dataset[0]) == 10:
      starting_gen = 1
    else:
      starting_gen = 0
  if miny == False:
    miny = 0
  if maxy == False:
    maxy = 1
  if y_label == False:
    y_label = "Score"
  if text != False and text_pos == False:
    text_pos = 'bottom'
  if experiment == False:
    experiment = 1
  if save_location == False:
    save_location = basics.desktop_location
  if save_name == False:
    save_name = 'plot.pdf'

  if dataset2 != False:
    if starting_gen2 == False:
      if len(dataset2[0]) == 10:
        starting_gen2 = 1
      else:
        starting_gen2 = 0
    if type(miny2) == bool and miny2 == False:
      miny2 = miny
    if type(maxy2) == bool and maxy2 == False:
      maxy2 = maxy
    if experiment2 == False:
      experiment2 = experiment
  plot(dataset, False, starting_gen, miny, maxy, y_label, text, conf, experiment, text_pos, save_location+save_name, dataset2, starting_gen2, miny2, maxy2, y_label2, text2, conf2, experiment2)



def mean(dataset, starting_gen=False, miny=False, maxy=False, y_label=False, text=False, conf=False, experiment=False, text_pos=False, save_location=False, save_name=False, dataset2=False, starting_gen2=False, miny2=False, maxy2=False, y_label2=False, text2=False, conf2=False, experiment2=False):
  
  if starting_gen == False:
    if len(dataset[0]) == 10:
      starting_gen = 1
    else:
      starting_gen = 0
  if type(miny) == bool and miny == False:
    miny = 0
  if type(maxy) == bool and maxy == False:
    maxy = 1
  if y_label == False:
    y_label = "Score"
  if text != False and text_pos == False:
    text_pos = 'bottom'
  if experiment == False:
    experiment = 1
  if save_location == False:
    save_location = basics.desktop_location
  if save_name == False:
    save_name = 'plot.pdf'

  if dataset2 != False:
    if starting_gen2 == False:
      if len(dataset2[0]) == 10:
        starting_gen2 = 1
      else:
        starting_gen2 = 0
    if type(miny2) == bool and miny2 == False:
      miny2 = miny
    if type(maxy2) == bool and maxy2 == False:
      maxy2 = maxy
    if experiment2 == False:
      experiment2 = experiment

  plot(dataset, True, starting_gen, miny, maxy, y_label, text, conf, experiment, text_pos, save_location+save_name, dataset2, starting_gen2, miny2, maxy2, y_label2, text2, conf2, experiment2)


def mean_with_chains(matrix1, matrix2, matrix3, starting_gen=1, miny=0.0, maxy=1.0, y_label="Score", conf=False, save=False):
  
  # Initialize figure
  plt.figure(1)

  # Replace NaN with None if present in the matrices
  matrix1 = RemoveNaN(matrix1)
  matrix2 = RemoveNaN(matrix2)
  matrix3 = RemoveNaN(matrix3)

  plt.subplots(figsize=(5.5, 3.0))
  ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5)

  n = len(matrix1[0])
  colours = ['red', 'blue', 'green']
  xvals = range(starting_gen, n+starting_gen)

  if conf == True:
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if miny < -2.0:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  elif type(conf) == int:
    plt.plot(range(-1,n+2), [conf] * (n+3), color='gray', linestyle=':', linewidth=0.5)

  x_vals = range(starting_gen, len(matrix1[0])+starting_gen)

  means, errors = MeanWithErrors(matrix1)
  _, caps, _ = ax1.errorbar(x_vals, means, yerr=errors, markersize=3.0, color='red', linestyle="-", linewidth=line_thickness, capsize=1, elinewidth=0.5, label='Experiment 1')

  means, errors = MeanWithErrors(matrix2)
  _, caps, _ = ax1.errorbar(x_vals, means, yerr=errors, markersize=3.0, color='green', linestyle="-", linewidth=line_thickness, capsize=1, elinewidth=0.5, label='Experiment 2')
  
  means, errors = MeanWithErrors(matrix3)
  _, caps, _ = ax1.errorbar(x_vals, means, yerr=errors, markersize=3.0, color='blue', linestyle="-", linewidth=line_thickness, capsize=1, elinewidth=0.5, label='Experiment 3')

  labels = range(starting_gen, starting_gen+n)
  plt.xlim(starting_gen-0.5, n+starting_gen-0.5)
  plt.ylim(miny, maxy)
  plt.xticks(xvals, labels, fontsize=axis_font_size)
  plt.yticks(fontsize=axis_font_size)
  plt.xlabel("Generation number", fontsize=label_font_size)
  plt.ylabel(y_label, fontsize=label_font_size)
  plt.tick_params(axis='x', which='both', bottom='off', top='off')

  ax3 = plt.subplot2grid((6,1), (5,0))
  plt.axis('off')
  handles, labels = ax1.get_legend_handles_labels()
  ax3.legend(handles, labels, loc='upper center', frameon=False, prop={'size':legend_font_size}, ncol=4, numpoints=1)


  plt.tight_layout(pad=0.2, w_pad=1.0, h_pad=0.00)

  plt.savefig(save)
  plt.clf()

def MeanWithErrors(matrix):
  means = []
  errors = []
  for i in range(0,len(matrix[0])):
    column = [row[i] for row in matrix if row[i] != None]
    means.append(np.mean(column))
    errors.append((np.std(column) / np.sqrt(len(column))) * 1.959964)
  return means, errors


def RemoveNaN(matrix):
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

def triple(matrix1, matrix2, matrix3, starting_gen=1, miny=0.0, maxy=1.0, y_label="Score", conf=False, save_location=False, save_name='plot.pdf'):
  
  # Initialize figure
  plt.figure(1)

  # Replace NaN with None if present in the matrices
  matrix1 = RemoveNaN(matrix1)
  matrix2 = RemoveNaN(matrix2)
  matrix3 = RemoveNaN(matrix3)

  plt.subplots(figsize=(5.5, 3.0))

  ax1 = plt.subplot2grid((4,3), (0,0), rowspan=3)
  n = len(matrix1[0])
  if conf == True:
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if miny < -2.0:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  elif type(conf) == int:
    plt.plot(range(-1,n+2), [conf] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  for i in range(0, len(matrix1)):
    x_vals = range(starting_gen, len(matrix1[i])+starting_gen)
    y_vals = [item for item in matrix1[i]]
    plt.plot(x_vals, y_vals, color=colours_by_experiment[0][i], marker=markers_by_chain[i], markersize=5.0, markeredgecolor=colours_by_experiment[0][i], linewidth=line_thickness, label='Chain ' + ascii_uppercase[i:i+1])
  labels = range(starting_gen, starting_gen+n)
  plt.xlim(starting_gen-0.5, n+starting_gen-0.5)
  plt.ylim(miny, maxy)
  plt.xticks(range(starting_gen, len(matrix1[0])+starting_gen), labels, fontsize=axis_font_size)
  plt.yticks(fontsize=axis_font_size)
  plt.xlabel("Generation number", fontsize=label_font_size)
  plt.ylabel(y_label, fontsize=label_font_size)
  plt.tick_params(axis='x', which='both', bottom='off', top='off')
  text_y = maxy - ((abs(miny-maxy)/15.)*1.45)
  plt.text(starting_gen, text_y, '(A)', {'fontsize':8}, fontweight='bold')
  handles, labels = ax1.get_legend_handles_labels()

  ax1_l = plt.subplot2grid((4,3), (3,0))
  plt.axis('off')
  ax1_l.set_yticklabels([])
  ax1_l.set_xticklabels([])
  ax1_l.legend([handles[0], handles[2], handles[1], handles[3]], [labels[0], labels[2], labels[1], labels[3]], loc='upper center', frameon=False, prop={'size':7.5}, ncol=2, numpoints=1, handletextpad=0.2)


  ax2 = plt.subplot2grid((4,3), (0,1), rowspan=3)
  n = len(matrix2[0])
  if conf == True:
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if miny < -2.0:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  elif type(conf) == int:
    plt.plot(range(-1,n+2), [conf] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  for i in range(0, len(matrix2)):
    x_vals = range(starting_gen, len(matrix2[i])+starting_gen)
    y_vals = [item for item in matrix2[i]]
    plt.plot(x_vals, y_vals, color=colours_by_experiment[1][i], marker=markers_by_chain[i], markersize=5.0, markeredgecolor=colours_by_experiment[1][i], linewidth=line_thickness, label='Chain ' + ascii_uppercase[4+i:i+5])
  labels = range(starting_gen, starting_gen+n)
  plt.xlim(starting_gen-0.5, n+starting_gen-0.5)
  plt.ylim(miny, maxy)
  plt.xticks(x_vals, labels, fontsize=axis_font_size)
  plt.yticks(fontsize=axis_font_size)
  plt.xlabel("Generation number", fontsize=label_font_size)
  plt.ylabel('')
  plt.tick_params(axis='x', which='both', bottom='off', top='off')
  ax2.set_yticklabels([])
  plt.text(starting_gen, text_y, '(B)', {'fontsize':8}, fontweight='bold')
  handles, labels = ax2.get_legend_handles_labels()

  ax2_l = plt.subplot2grid((4,3), (3,1))
  plt.axis('off')
  ax2_l.set_yticklabels([])
  ax2_l.set_xticklabels([])
  ax2_l.legend([handles[0], handles[2], handles[1], handles[3]], [labels[0], labels[2], labels[1], labels[3]], loc='upper center', frameon=False, prop={'size':7.5}, ncol=2, numpoints=1, handletextpad=0.2)


  ax3 = plt.subplot2grid((4,3), (0,2), rowspan=3)
  n = len(matrix3[0])
  if conf == True:
    plt.plot(range(-1,n+2), [1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
    if miny < -2.0:
      plt.plot(range(-1,n+2), [-1.959964] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  elif type(conf) == int:
    plt.plot(range(-1,n+2), [conf] * (n+3), color='gray', linestyle=':', linewidth=0.5)
  for i in range(0, len(matrix3)):
    x_vals = range(starting_gen, len(matrix3[i])+starting_gen)
    y_vals = [item for item in matrix3[i]]
    plt.plot(x_vals, y_vals, color=colours_by_experiment[2][i], marker=markers_by_chain[i], markersize=5.0, markeredgecolor=colours_by_experiment[2][i], linewidth=line_thickness, label='Chain ' + ascii_uppercase[8+i:i+9])
  labels = range(starting_gen, starting_gen+n)
  plt.xlim(starting_gen-0.5, n+starting_gen-0.5)
  plt.ylim(miny, maxy)
  plt.xticks(x_vals, labels, fontsize=axis_font_size)
  plt.yticks(fontsize=axis_font_size)
  plt.xlabel("Generation number", fontsize=label_font_size)
  plt.ylabel('')
  plt.tick_params(axis='x', which='both', bottom='off', top='off')
  ax3.set_yticklabels([])
  plt.text(starting_gen, text_y, '(C)', {'fontsize':8}, fontweight='bold')
  handles, labels = ax3.get_legend_handles_labels()

  ax3_l = plt.subplot2grid((4,3), (3,2))
  plt.axis('off')
  ax3_l.set_yticklabels([])
  ax3_l.set_xticklabels([])
  ax3_l.legend([handles[0], handles[2], handles[1], handles[3]], [labels[0], labels[2], labels[1], labels[3]], loc='upper center', frameon=False, prop={'size':7.5}, ncol=2, numpoints=1, handletextpad=0.2)
  
  plt.tight_layout(pad=0.2, w_pad=1.0, h_pad=0.00)

  if save_location == False:
    save_location = basics.desktop_location

  plt.savefig(save_location + save_name)
  plt.clf()