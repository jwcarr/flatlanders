<?php

// Generate MAP if one hasn't been set up yet
if ($_REQUEST['map'] == '') {
  include('php/generateMap.php');
  $map = generateMap($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen']);
}
else {
  $map = $_REQUEST['map'];
}

// Parse the map
$parsed_map = parseMap($map);
$new_map = $parsed_map[0];
$experiment_page = $parsed_map[1];
$item_info = $parsed_map[2];

// Set window location for next page for use in JavaScript
$window_location = 'index.php?page=experiment&subject='. $_REQUEST['subject'] .'&cond='. $_REQUEST['cond'] .'&chain='. $_REQUEST['chain'] .'&gen='. $_REQUEST['gen'] .'&map='. $new_map;

// If this is a BEGIN PAGE
if ($experiment_page == 'BEGIN') {
  // Clear the data files in case they already contain content
  clearFiles($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen']);
}

// If this is a TRAINING PAGE
elseif ($experiment_page == 'TR') {
  // Get the relvant training word from previous participant's dynamic set file
  $training_word = getWord($_REQUEST['cond'], $_REQUEST['chain'], ($_REQUEST['gen']-1), $item_info);

  // Get the XY coordinates for the relevant triangle from the previous participant's dynamic set file
  $xy = loadTriangle($_REQUEST['cond'], $_REQUEST['chain'], ($_REQUEST['gen']-1), 'd', $item_info);

  // If is the first training item...
  if ($_REQUEST['first_training_item'] == 'yes') {
    // Write log to the "training" file
    saveLogData($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['subject'], "Cond.\tChain\tGen.\tSub.\tTimestamp\n". $_REQUEST['cond']. "\t". $_REQUEST['chain'] ."\t". $_REQUEST['gen'] ."\t". $_REQUEST['subject'] ."\t". date("d/m/Y H:i:s") . "\n\n" . $map ."\n");
  }

  // If a mini test answer has been provided...
  if ($_REQUEST['a'] != '') {
    // Write it to the log along with the correct answer
    saveLogData($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['subject'], $_REQUEST['correct_answer'] ."\t". $_REQUEST['a']);
  }

}

// If this is a MINI-TEST PAGE
elseif ($experiment_page == 'MT') {
  // Get the XY coordinates for for the random chosen stimulus from the previous participant's dynamic set file
  $xy = loadTriangle($_REQUEST['cond'], $_REQUEST['chain'], ($_REQUEST['gen']-1), 'd', $item_info);
  // Get the correct word for the randomly chosen stimulus
  $correct_answer = getWord($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen']-1, $item_info);
}

// If this is a TEST PAGE
elseif ($experiment_page == 'TS') {
  // Parse the test item information into its set (either 'd' or 's') and the stimulus number from that set
  $stimulus_info = explode('.', $item_info);
  $stimulus_set = $stimulus_info[0];
  $stimulus_number = $stimulus_info[1];

  // If the current test item belongs to the dynamic flow...
  if ($stimulus_set == 'd') {
    // Generate random XY coordinates
    $xy = generateTriangle();
  }
  // Otherwise, if the current test item belongs to the stable flow...
  else {
    // Load the XY coordinates for the relevant triangle from the stable set file
    $xy = loadTriangle($_REQUEST['cond'], $_REQUEST['chain'], ($_REQUEST['gen']-1), 's', $stimulus_number);
  }

  // If the participant is in condition 2 and the current test item belongs to the dynamic set...
  if ($_REQUEST['cond'] == 2 AND $stimulus_set == 'd') {
    // Get the words that the participant has used so far
    $words = getWords($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen']);

    // Count the total number of words that have been used so far
    $n = count($words);

    // Set up an empty array into which to put overused words
    $overused_words = array();

    // Add each word that has been overused to the $overused_words array
    for ($i=0; $i<$n; $i++) {
      $c=1;
      for ($j=$i+1; $j<$n; $j++) {
        if ($words[$i] == $words[$j]) {
          $words[$j] = $i." ".$j;
          $c = $c+1;
        }
      }
      if ($c == $permitted_word_repetitions) { $overused_words[] = $words[$i]; }
    }
  }

  // If this is not the first test item (indicated by the fact that $current is set to nothing), do the following...
  if ($_REQUEST['current'] != '') {
    // Create an XY array from the previous XY coordinates
    $last_xy = array($_REQUEST['last_x1'], $_REQUEST['last_x2'], $_REQUEST['last_x3'], $_REQUEST['last_y1'], $_REQUEST['last_y2'], $_REQUEST['last_y3']);

    // Save the previous answer to the relevant file
    saveAnswer($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['current'], $_REQUEST['a'], $last_xy);
  }

}

elseif ($experiment_page == 'DR') {
  // Parse the test item information into its set (either 'd' or 's') and the stimulus number from that set
  $stimulus_info = explode('.', $item_info);
  $stimulus_set = $stimulus_info[0];
  $stimulus_number = $stimulus_info[1];

  // If the current test item belongs to the dynamic flow...
  if ($stimulus_set == 'd') {
    // Generate random XY coordinates
    $xy = generateTriangle();
  }
  // Otherwise, if the current test item belongs to the stable flow...
  else {
    // Load the XY coordinates for the relevant triangle from the stable set file
    $xy = loadTriangle($_REQUEST['cond'], $_REQUEST['chain'], ($_REQUEST['gen']-1), 's', $stimulus_number);
  }
}

// If this is a MATCHER PAGE
elseif ($experiment_page == 'MR') {
  // Parse the test item information into its set (either 'd' or 's') and the stimulus number from that set
  $stimulus_info = explode('.', $item_info);
  $stimulus_set = $stimulus_info[0];
  $stimulus_number = $stimulus_info[1];

  // Generate a set of random distractor triangles for the matcher array
  $triangle_array = generateTriangleArray();

  // For each distractor triangle
  foreach ($triangle_array as $triangle) {
    // add its coordinates to the
    $triangle_array_JS .= implode(',', $triangle).',';
  }

  // If this is not the first test item (indicated by the fact that $current is set to nothing), do the following...
  if ($_REQUEST['current'] != '') {
    // Create an XY array from the previous XY coordinates
    $last_xy = array($_REQUEST['last_x1'], $_REQUEST['last_x2'], $_REQUEST['last_x3'], $_REQUEST['last_y1'], $_REQUEST['last_y2'], $_REQUEST['last_y3']);

    $sel_xy = array($_REQUEST['cord_x1'], $_REQUEST['cord_x2'], $_REQUEST['cord_x3'], $_REQUEST['cord_y1'], $_REQUEST['cord_y2'], $_REQUEST['cord_y3']);

    // Save the previous answer to the relevant file
    saveCommAnswer($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['current'], $_REQUEST['a'], $last_xy, $_REQUEST['sub'], $sel_xy);
  }
}

// If this is a BREAK PAGE or WAIT PAGE
elseif ($experiment_page == 'BREAK' OR $experiment_page == 'WAIT') {
  // Write the final mini-test answer to the log
  saveLogData($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['subject'], $_REQUEST['correct_answer'] ."\t". $_REQUEST['a']);
}

// If this is an END PAGE
elseif ($experiment_page == 'END') {
  // Create an XY array from the previous XY coordinates
  $last_xy = array($_REQUEST['last_x1'], $_REQUEST['last_x2'], $_REQUEST['last_x3'], $_REQUEST['last_y1'], $_REQUEST['last_y2'], $_REQUEST['last_y3']);

  $sel_xy = array($_REQUEST['cord_x1'], $_REQUEST['cord_x2'], $_REQUEST['cord_x3'], $_REQUEST['cord_y1'], $_REQUEST['cord_y2'], $_REQUEST['cord_y3']);

  if ($_REQUEST['cond'] == 3) {
    if ($_REQUEST['sub'] == 'SubB') {
      saveFinalCommAnswer($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['current'], $_REQUEST['a'], $last_xy, $_REQUEST['sub'], $sel_xy);
    }
  }
  else {
    // Save the final answer (and sort the stable data file back to its unshuffled order)
    saveFinalAnswer($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['current'], $_REQUEST['a'], $last_xy);
  }

  // Write time at whcih the experiment ended to log along with overuse count if condition 2
  if ($_REQUEST['cond'] == 2) {
    saveLogData($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['subject'], "\nOveruse count = ". $_REQUEST['overuse'] ."\n\nEND AT " . date("d/m/Y H:i:s") . "\n-------------------------------------------------------\n\n");
  }
  else {
    saveLogData($_REQUEST['cond'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['subject'], "\nEND AT " . date("d/m/Y H:i:s") . "\n-------------------------------------------------------\n\n");
  }
}

if ($show_score == True) {
  if ($experiment_page == 'DR' OR $experiment_page == 'MR') {
    $points = $_REQUEST['score'] * 10;
  }
}

?>
