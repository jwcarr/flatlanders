<?php

// List of valid chain codes for each experiment (default = [A, B, C, D], [E, F, G, H], and [I, J, K, L])
$chain_codes = array(array('A', 'B', 'C', 'D'), array('E', 'F', 'G', 'H'), array('I', 'J', 'K', 'L'));

// Maximum generation number (default = 10)
$max_generation_number = 10;

// Magnitude of the stimuli sets (default = 48)
$set_size = 48;

// Amount of time for each training item in milliseconds (default = 5000)
$time_per_training_item = 5000;

// Delay before showing the training word in milliseconds (default = 1000)
$word_delay = 1000;

// Length of time to show mini-test feedback in milliseconds (default = 1000)
$mini_test_feedback_time = 1000;

// Length of time to show communication feedback in milliseconds (default = 5000)
$communication_feedback_time = 3000;

// Amount of time for the break between training and testing in seconds (default = 30)
$break_time = 30;

// Canvas size in pixels for the triangle stimuli (width by height) (default = 500x500)
$canvas_size = array(500, 500);

// Width of the unusable boarder area around the canvas in pixels (default = 10)
$canvas_border = 10;

// Thickness of the trianlge lines in pixels (default = 2)
$triangle_line_thickness = 2;

// Radius of the orienting spot in pixels (default = 8)
$orienting_spot_radius = 8;

// Number of times a word can be reused to label items in the dynamic set (experiment 2 only) (default = 3)
$permitted_word_repetitions = 3;

// Do a mini test every X items during the training phase (default = 3, must be a divisor of $set_size)
// Note, this also determines the number of passes over the training data, ensuring that each item is mini-tested exactly once
$mini_test_frequency = 3;

// Number of trianlges to show in the matcher array (columns by rows) (experiment 3 only)
$triangle_array_size = array(3, 2);

// Show a running score on the director/matcher pages for the number of stimuli correctly matched (default = True)
$show_score = True;

// IP address for the webserver (experiment 3 only)
$server_ip = '192.168.1.70';

// Port to use for the node.js server (experiment 3 only)
$node_port = '8080';

// Skip over the training section of the experiment (for testing purposes only)
$skip_training = False;

// Set timezone for timestamps (default = UTC)
date_default_timezone_set('UTC');

?>
