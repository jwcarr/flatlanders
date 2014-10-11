<?php

// Check that the chain code belongs to the global set of valid chain codes for the selected experiment
function checkChain($condition, $chain_code) {
  global $chain_codes;
  if (in_array($chain_code, $chain_codes[$condition-1]) == True) { return True; } else { return False; }
}

// Check that the generation number does not exceed the global maximum generation number (and is greater than 0)
function checkGen($generation_number) {
  global $max_generation_number;
  if ($generation_number > 0 AND $generation_number <= $max_generation_number) { return True; } else { return False; }
}

// Check that the output data files exist and are writeable
function checkOutputFiles($condition, $chain_code, $generation) {
  $dynamic_file = is_writable("data/". $condition ."/" . $chain_code ."/" . $generation ."d");
  $stable_file = is_writable("data/". $condition ."/" . $chain_code ."/" . $generation ."s");
  if ($dynamic_file == True AND $stable_file == True) { return True; } else { return False; }
}

// Check that the input data files contain the correct number of lines (i.e. $set_size number of lines)
function checkInputSet($condition, $chain_code, $generation) {
  global $set_size;
  $lines = loadFile($condition, $chain_code, ($generation-1), "d");
  if (count($lines) == $set_size) { return True; } else { return False; }
}

// Check that the required sound files are present and accounted for
function checkSoundFiles($words) {
  // Set up an array to dump a list of missing sound files
  $missing_words = array();
  // For each word that needs a vocalization...
  for ($i = 0; $i < count($words); $i++) {
    // ... check that a sounds file exists
    if (file_exists("vocalizations/". $words[$i] .".m4a") == False) {
      // If not, add it to the missing words array
      $missing_words[] = $words[$i] . ".m4a";
    }
  }
  // Return the array of missing words
  return $missing_words;
}

// Function to output a row on the validation page
function validationTableRow($colour, $message) {
  return "<div id='parameter'><img src='images/". $colour .".png' width='16' height='16' alt='light' /> ". $message ."</div>";
}

// Check that the chain code is valid
if (checkChain($_REQUEST["condition"], $_REQUEST["chain"]) == True) { echo validationTableRow("green", "Chain " . $_REQUEST["chain"]); }
else { echo validationTableRow("red", "Chain \"". $_REQUEST["chain"] ."\" is invalid"); $error_count ++; }

// Check that the generation number is valid
if (checkGen($_REQUEST["gen"]) == True) { echo validationTableRow("green", "Generation " . $_REQUEST["gen"]); }
else { echo validationTableRow("red", "Generation \"". $_REQUEST["gen"] ."\" is invalid"); $error_count ++; }

// Check the condition number is valid
if ($_REQUEST["condition"] == 1 OR $_REQUEST["condition"] == 2 OR $_REQUEST["condition"] == 3) { echo validationTableRow("green", "Experiment " . $_REQUEST["condition"]); }
else { echo validationTableRow("red", "Condition \"". $_REQUEST["condition"] ."\" is invalid"); $error_count ++; }

// Check that there are $set_size words in the input set
if (checkInputSet($_REQUEST["condition"], $_REQUEST["chain"], $_REQUEST["gen"]) == True) { echo validationTableRow("green", "Words in the input set are valid"); }
else { echo validationTableRow("red", "Input file does not contain $set_size words"); $error_count ++; }

// Check that the data files exist for writing
if (checkOutputFiles($_REQUEST["condition"], $_REQUEST["chain"], $_REQUEST["gen"]) == True) { echo validationTableRow("green", "Output data files are ready for writing"); }
else { echo validationTableRow("red", "Output data files at <i>/data/" . $_REQUEST["condition"] . "/" . $_REQUEST["chain"] . "/</i> are not writeable. Check Permissions"); $error_count ++; }

// Check that sound files exist for the words in the input set
$words = getWords($_REQUEST["condition"], $_REQUEST["chain"], ($_REQUEST["gen"]-1));
$missing_words = checkSoundFiles($words);
if (count($missing_words) == 0) { echo validationTableRow("green", "Required sound files are available"); }
else {
  // If there are missing words, output a list of them
  for ($i=0; $i < count($missing_words); $i++) {
    $missing_words_list = $missing_words_list . $missing_words[$i] . ", ";
  }
  echo validationTableRow("red", "The following sound files are missing: " . substr($missing_words_list, 0, -2));
  $error_count ++;
}

// If the above validation functions produce no errors, display messages to check the volume level and keyboard layout
if ($error_count == 0) {
  // Sound warning
  echo validationTableRow("orange", "Is the volume level okay? <a href=\"javascript:document.getElementById('alex').play()\">test</a>");

  // Keyboard layout warning
  echo validationTableRow("orange", "Are you using the Alpha-only keyboard layout?");

  // Keyboard layout warning
  echo validationTableRow("orange", "Is the node.js server running?");
}

?>
