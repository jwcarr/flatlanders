flatlanders
===========


Description
-----------

Code for conducting a series of experiments looking at the evolution of language structure in an open-ended meaning space through iterated learning. More information to follow.


Repository Content
------------------

The repository contains the following directories:

- ```/analysis```: Python code for analyzing the data.

- ```/data```: Plain text files containing the data for the three experiments and the two rating tasks.

- ```/experiment```: HTML, JavaScript, and PHP code for running the experiments.

- ```/rating_tasks```: HTML, JavaScript, and PHP code for running the online rating tasks.


Analytical Code
---------------

The ```/analysis``` directory contains Python code for analyzing the three experiments and the two rating tasks. The Python modules are listed below with a brief description. See below for examples of how to use the code.

- ```basics.py```: Basic functions called from various other modules; mainly used for loading in data.

- ```communication.py```: Functions for retrieving and plotting communicative accuracy and communicative error results, and for analyzing the data from the second online ratings task.

- ```expressivity.py```: Functions for retrieving and plotting expressivity results.

- ```geometrical_distance.py```: Functions for computing the geometrical dissimilarity between pairs of triangles.

- ```geometry.py```: Various basic geometrical functions for dealing with triangles.

- ```initial_set_generator.py```: Code for producing an initial Generation-0 set file used to initiate a chain.

- ```Krippendorff.py```: Module for computing Krippendorff’s alpha coefficient. Adapted from: http://grrrr.org/2011/05/31/krippendorff_alpha-python/

- ```language_generator.py```: Functions for generating an initial Generation-0 randomized language.

- ```Mantel.py```: Module for running a Mantel test on two distance matrices.

- ```mds.py```: Module for computing an MDS solution to the naïve raters’ dissimilarity ratings and producing Voronoi-tessellated plots and triangle graphics.

- ```Page.py```: Module for running Page’s test.

- ```plot.py```: Module that interfaces with Matplotlib for producing plots of a consistent style.

- ```rater_analysis.py```: Functions for analyzing the dissimilarity data from the naïve raters and forming a distance matrix that can be used by other modules.

- ```rater_generator.py```: Functions for generating the stimulus sets for naïve raters in Tasks 1 and 2 to work on.

- ```sound_symbolism.py```: Functions for analyzing sound symbolism.

- ```structure_measure_comparison.py```: Code for plotting a comparison of the general and sublexical structure measures.

- ```structure.py```: Functions for computing and plotting structure results.

- ```sublexical_structure.py```: Module for measuring sublexical structure.

- ```svg_polygons.py```: A simple class for drawing polygons and saving to an SVG file.

- ```transmission_error.py```: Functions for computing and plotting transmission error results.

- ```vocalize.py```: Functions for transforming a string into a synthesized vocalization using the Apple MacinTalk speech synthesizer.

- ```Voronoi.py```: Module for creating a Voronoi tessellation. Adapted from: https://gist.github.com/neothemachine/8803860


Raw Data
--------

The ```/data``` directory contains subdirectories for the three experiments and the two rating tasks. The experiment directories are further divided into subdirectories for each chain.

### Experiment data

The directory for each chain contains 32 plain text files. The initial number in the filename refers to the generation number, which is followed by ```d``` (dynamic set), ```s``` (static set), or ```log``` (log file). Dynamic set files list the 48 words used by the participant to label the dynamic set, alongside coordinates for the corresponding triangles (*x*-coordinate and *y*-coordinate for vertices 1, 2, and 3; vertex 1 is always the orienting spot), and a timestamp for when the response was submitted. The lines of the file are in order of presentation. Static set files follow the same organization, except they are ordered according to an arbitrary number assigned to each triangle in the static set and contain an additional column which gives the order of presentation. The order of static set files is the same for all participants, meaning that the strings in consecutive static set files can be compared directly.

Log files contain some header information, including a timestamp marking the beginning of the training phase, followed by a long sequence that describes the order in which items were presented throughout the experiment (```TR``` = training item, ```MT``` = mini-test item, ```TS-d``` = test on a dynamic set item, ```TS-s``` = test on a static set item). This sequence is followed by the mini-test results (target answer and typed answer separated by tabs) and finally a timestamp for the end of the experiment. These files are exactly the same for Experiment 2, except the log file contains an additional line near the bottom which gives a count of the number of times the participant was told to enter a different word during their test phase.

The Experiment 3 data (42 files per chain) is organized in the same way as described above with the following two exceptions: (1) the dynamic and static set files contain additional columns giving the coordinates of the triangle selected from the matcher array, and (2) there are two log files per generation marked with ```SubA``` and ```SubB``` for subjects A and B respectively. Subject A is always the first participant to be the director and labels the dynamic set; subject B always labels the static set.

### Rating task data

The ```/task_1``` directory contains 96 plain text files, one for each of the participants who completed the first dissimilarity rating task. The filename is a unique “rater ID” used to identify participants. The first line gives the current trial number (the task is complete, so this will always read 151), the direction in which the sliding scale was oriented (```L``` = *very similar* on the left; ```R``` = *very similar* on the right), the participant’s IP address (all IP addresses have been concealed), and a Unix timestamp for the time the task was started. The subsequent lines give the results for each of the 150 rating trials. The first six trials are practice trials; in addition, three reliability trials are randomly interspersed among the normal trials. Column 1 gives a reference number for the triangle in the static set presented on the left; column 2 gives the reference number for the triangle presented on the right; column 3 gives the participant’s rating on the 1,000 point scale (0 is always *very similar* and 1000 is always *very dissimilar* regardless of the direction of the sliding scale); and column 4 gives a Unix timestamp for the time the rating was submitted. Negative reference numbers refer to a small fixed set of triangles used only in practice and reliability trials. The final line in the file is a unique code generated at the time the participant finished the task allowing him or her to collect payment. In some cases, the rating is given as ```undefined```; this was caused by a browser compatibility issue that was later fixed.

The ```/task_2``` directory contains 184 files, one for each of the participants who completed the second dissimilarity rating task. The contents of the files are organized in the same way as described above with the following exceptions: (1) Task 2 is comprised of 135 or 136 trials rather than 150, and (2) the coordinates of each triangle are given in full for each trial rather then represented by reference numbers, since the triangles rated in this task are not drawn from a fixed set as in the case in Task 1.


Replicating the Reported Results
--------------------------------

All analytical code is written in Python and has only been tested under version 2.7 of the language. The following nonstandard libraries are used extensively throughout the codebase and should be installed first (if not already available):

- Matplotlib: http://matplotlib.org

- NumPy: http://www.numpy.org

- SciPy: https://www.scipy.org

All analyses were performed on OS X, but the instructions that follow should also apply to Linux or Windows systems. The instructions begin with the assumption that you have ```cd```’d into the ```analysis/``` directory and opened a Python interpreter, e.g.:

```
$ cd flatlanders/analysis/
$ python
```

These instructions are intended to get you started and do not cover the use of every function in every module.

### Expressivity

The following commands are used to import the ```expressivity``` module, load in the expressivity data for the dynamic and static sets of all generations in Experiment 1, and produce a plot displaying the results.

```python
import expressivity
E1_exp_dynamic = expressivity.experiment_results(1, set_type='d')
E1_exp_static = expressivity.experiment_results(1, set_type='s')
expressivity.plot(E1_exp_dynamic, E1_exp_static, experiment=1)
```

By default the plot will be saved to your desktop, although this can be changed by passing a path to the ```plot``` function using the ```save_location``` argument or by editing the ```desktop_location``` variable in ```basics.py```. To run the analysis on Experiment 2 or 3, change all ```1```s to ```2```s or ```3```s. To get expressivity results for the union of the dynamic and static set the ```set_type``` argument to ```'c'```.

### Structure

The following commands are used to import the ```structure``` module, compute the structure results for Experiment 1, and produce a plot displaying the results.

```python
import structure
E1_str = structure.experiment_results(1, sublexical=False, permutations=1000)
E1_sub = structure.experiment_results(1, sublexical=True, permutations=1000)
structure.plot(E1_str, E1_sub, experiment=1)
```

The results reported in the paper are based on 100,000 permutations. However, 1,000 should be sufficient to replicate the results quickly. N.B., the computation of the measure of sublexical structure is around an order of magnitude slower than the measure of general structure.

### Transmission error

The following commands are used to import the ```transmission_error``` module, compute the results for Experiment 1, and produce a plot.

```python
import transmission_error
E1_trans_error = transmission_error.experiment_results(1)
transmission_error.plot(E1_trans_error, experiment=1)
```

### Sound symbolism

The following commands are used to import the ```sound_symbolism``` module, compute the results for Experiment 1, and produce a plot.

```python
import sound_symbolism
E1_ss_shape = sound_symbolism.experiment_results(1, symbolism='shape')
E1_ss_size = sound_symbolism.experiment_results(1, symbolism='size')
sound_symbolism.plot(E1_ss_shape, E1_ss_size, experiment=1)
```

### Communicative accuracy

The following commands are used to import the ```communication``` module, compute the communicative accuracy and error results for Experiment 3 (n.b., communication only applies to Experiment 3), and produce a plot.

```python
import communication
E3_comm_acc = communication.accuracy_results()
E3_comm_err = communication.error_results()
communication.plot(E1_comm_acc, E1_comm_err)
```

### Page’s test

To run Page’s test on any of the data, import the ```Page``` module and pass a data matrix that was computed above to the ```test``` function. For example, to run Page’s test on the results for structure that we generated above, run:

```python
import Page
Page.test(E1_str, ascending=True)
```

The ```ascending``` argument defines whether we are hypothesizing an upward on downward trend (in this case an upward trend).

### MDS plots

The MDS plots and triangle visualizations are produced using the code in ```mds.py```. This module requires two nonstandard libraries to be installed:

- scikit-learn: http://scikit-learn.org

- Polygon: http://www.j-raedler.de/projects/polygon/

The following generates a graphic for Generation 10 in Chain A with the default parameters:

```python
import mds
mds.plot('A', 10)
```

N.B., this will not produce the same set of colors shown in the paper; a unique color palette is determined on each run. To get multiple color candidates set the ```colour_candidates``` argument to the number of candidates you want and then pick your favorite. To generate plots for an entire chain or experiment, use one of the following:

```python
mds.plot_chain('A'):
mds.plot_experiment(1)
```

The ```plot```, ```plot_chain```, and ```plot_experiment``` functions can take a variety of arguments to further refine the plots:

-   The ```chain_wide_palette``` argument determines whether the color palette is selected based on the string distances across an entire chain or within each generation. Setting this to ```True``` is useful if you want to be able to compare across generations.

-   The ```spectrum``` argument determines how much of the color spectrum to use, allowing you to avoid extremely light and extremely dark colors which often don’t work very well.

-   The ```push_factor``` argument artificially makes colors more distinct, which is useful if you’re using a chain-wide palette where colors
    can become too similar to interpret.

-   The ```show_prototypes``` argument adds prototype triangles to the triangle graphics.

-   The ```label_cells``` argument adds string labels to the Voronoi cells.

-   The ```join_contiguous_cells``` argument joins together cells that form a continuous region of one color. However, this does not always work correctly, so use with caution.

### Geometrical measure of triangle dissimilarity

The code for computing a geometrical measure of dissimilarity between triangles is contained in ```geometrical_distance.py```. When this module is run, it automatically computes distance matrices for all 15 combinations of the four geometrical features and stores them in a list called ```all_combination_matrices```. The last item in that list, ```all_combination_matrices[14]```, is the combination of all four features (i.e., Type 15). To plot the Experiment 1 results for structure using the combination of all four features, you can simply pass that matrix to the structure module:

```python
import geometrical_distance
import structure
E1_str_geo_all = structure.experiment_results(1, meaning_distances=geometrical_distance.all_combination_matrices[14])
```

Say you wanted to compare how the combination of all four features compares with the combination of just shape and size in terms of the result it has on the measure of structure. To do this, compute the structure results for the shape/size combination (Type 10 so index 9 in ```all_combination_matrices```):

```python
E1_str_geo_shpSiz = structure.experiment_results(1, meaning_distances=geometrical_distance.all_combination_matrices[9])
```

and then plot the results:

```python
structure.plot(E1_str_geo_all, E1_str_geo_shpSiz, experiment=1)
```

You should find that structure is better captured by the geometrical metric that only takes shape and size into account.

To find which combination of features provide the strongest correlation with the strings in for all generations of Experiment 1, use the ```experiment_results``` function and then ```latex_table``` to format as a LaTeX table, e.g.:

```python
E1_typology = geometrical_distance.experiment_results(1)
geometrical_distance.latex_table(E1_typology)
```

This saves a ```.tex``` file to your desktop containing the source for producing a full table.


License
-------

Unless otherwise noted, all code in this repository is licensed under the terms of the MIT License.
