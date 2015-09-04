<?php

// Open a file
function openFile($filename) {
  // If the file exists...
  if (file_exists($filename)) {
    // If the filesize > 0...
    if (filesize($filename) > 0) {
      // Open the file
      $file = fopen($filename, 'r');
      // If you can secure a read lock on the file...
      if (flock($file, LOCK_SH)) {
        // Read the data from the file...
        $data = fread($file, filesize($filename));
        // ... and then unlock, close, and return its contents
        flock($file, LOCK_UN);
        fclose($file);
        return $data;
      }
      // Failure to obtain a lock on the file, so close file and return False
      fclose($file);
      return False;
    }
    // Filesize is 0, so return null
    return '';
  }
  // The file does not exist, so return False
  return False;
}

// Write data to a file
function writeFile($filename, $data) {
  // If the file exists and is writeable...
  if (is_writable($filename)) {
    // Open the file
    $file = fopen($filename, 'w');
    // If you can secure a write lock on the file...
    if (flock($file, LOCK_EX)) {
      // If you succeed in writing the data to the file...
      if (fwrite($file, $data)) {
        // unlock, close, and return True
        flock($file, LOCK_UN);
        fclose($file);
        return True;
      }
      // Failure to write to the file, so unlock
      flock($file, LOCK_UN);
    }
    // Failure to obtain a lock on the file or to write to the file, so close
    fclose($file);
  }
  // The file does not exist or cannot write or cannot obtain lock, so return False
  return False;
}

// Load the file for a given participant's dynamic or stable set
function loadFile($condition, $chain_code, $generation, $set) {
  // Get the data from that file
  $data = openFile('../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation . $set);
  // Separate the raw data at line breaks
  $lines = explode("\n", $data);
  // Return the lines as an array
  return $lines;
}

// Get the words from a data file
function getWords($condition, $chain_code, $generation) {
  // Load in the file for a specific participant's dynamic set file
  $lines = loadFile($condition, $chain_code, $generation, 'd');
  // Set up an empty array in which to dump the words
  $words = array();
  // For each line in the data file...
  foreach ($lines as $line) {
    // Separate out the columns delimited by tabs
    $columns = explode("\t", $line);
    // Dump the first column (the word) into the $words array
    array_push($words, $columns[0]);
  }
  // Return the words as an array
  return $words;
}

// Get a specific word from a given participant's dynamic set file
function getWord($condition, $chain_code, $generation, $word_number) {
  // Get all words in that participant's dynamic file
  $words = getWords($condition, $chain_code, $generation);
  // Return the requested word
  return $words[$word_number];
}

// Save log data to the log file
function saveLogData($condition, $chain_code, $generation, $subject='', $new_data) {
  // Open the log file as it stands
  $data = openFile('../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation .'log'. $subject);
  if ($data == "") { $data = $new_data; } else { $data = $data ."\n". $new_data; }
  // Write out the new log file
  writeFile('../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation .'log'. $subject, $data);
}

// Save a test answer to a participant's dynamic or stable set file
function saveAnswer($condition, $chain_code, $generation, $position, $answer, $xy) {
  // Parse the map position into a set type ("d" or "s") and the stimulus number
  $position = explode('.', $position);
  // If saving a dynamic file...
  if ($position[0] == 'd') {
    // Concatenate the answer, XY coordinates, and timestamp (delimited by tabs)
    $answer = trim($answer) ."\t". $xy[0] .','. $xy[3] ."\t". $xy[1] .','. $xy[4] ."\t". $xy[2] .','. $xy[5] ."\t". date("H:i:s");
  }
  // If saving a stable file...
  else {
    // Concatenate the stimulus number, answer, XY coordinates, and timestamp (delimited by tabs)
    $answer = $position[1] .'|||'. trim($answer) ."\t". $xy[0] .','. $xy[3] ."\t". $xy[1] .','. $xy[4] ."\t". $xy[2] .','. $xy[5] ."\t". date("H:i:s");
  }
  // Determine the filename you want to write to
  $filename = '../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation . $position[0];
  // Read the content of that file as it currently stands
  $current_data = openFile($filename);
  // The new content of the file is the old data + the new answer
  $new_data = $current_data ."\n". $answer;
  // Write this new data to the file
 	writeFile($filename, trim($new_data));
}

// Save a test answer to a participant's dynamic or stable set file
function saveCommAnswer($condition, $chain_code, $generation, $position, $answer, $xy, $sel_xy) {
  // Parse the map position into a set type ("d" or "s") and the stimulus number
  $position = explode('.', $position);
  // If saving a dynamic file...
  if ($position[0] == 'd') {
    // Concatenate the answer, XY coordinates, and timestamp (delimited by tabs)
    $answer = trim($answer) ."\t". $xy[0] .','. $xy[3] ."\t". $xy[1] .','. $xy[4] ."\t". $xy[2] .','. $xy[5] ."\t". date("H:i:s") ."\t". $sel_xy[0] .','. $sel_xy[3] ."\t". $sel_xy[1] .','. $sel_xy[4] ."\t". $sel_xy[2] .','. $sel_xy[5];
  }
  // If saving a stable file...
  else {
    // Concatenate the stimulus number, answer, XY coordinates, and timestamp (delimited by tabs)
    $answer = $position[1] ."|||". trim($answer) ."\t". $xy[0] .','. $xy[3] ."\t". $xy[1] .','. $xy[4] ."\t". $xy[2] .','. $xy[5] ."\t". date("H:i:s") ."\t". $sel_xy[0] .','. $sel_xy[3] ."\t". $sel_xy[1] .','. $sel_xy[4] ."\t". $sel_xy[2] .','. $sel_xy[5];
  }
  // Determine the filename you want to write to
  $filename = '../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation . $position[0];
  // Read the content of that file as it currently stands
  $current_data = openFile($filename);
  // The new content of the file is the old data + the new answer
  $new_data = $current_data ."\n". $answer;
  // Write this new data to the file
   writeFile($filename, trim($new_data));
}

// Save the final test item, and then sort the stable set into its unshuffled order
function saveFinalAnswer($condition, $chain_code, $generation, $position, $answer, $xy) {
  // Import the global variable $set_size
  global $set_size;
  // Parse the map position into a set type ("d" or "s") and the stimulus number
  $position = explode('.', $position);
  // Load in the lines from a specific stable set file
  $lines = loadFile($condition, $chain_code, $generation, 's');
  // Concatenate the stimulus number, answer, XY coordinates, and timestamp (delimited by tabs) for the final test item
  $answer = $position[1] .'|||'. trim($answer) ."\t". $xy[0] .','. $xy[3] ."\t". $xy[1] .','. $xy[4] ."\t". $xy[2] .','. $xy[5] ."\t". date("H:i:s");
  // Add the final answer to the lines array
  array_push($lines, $answer);
  // Set up an empty array in which to dump the parsed lines
  $mappings = array();
  // For each line in the file...
  for ($i=0; $i < $set_size; $i++) {
    // Parse the line into its stimulus number and recorded data
    $parsed_line = explode('|||', $lines[$i]);
    // Put the recorded data into the $mappings array with a key equal to the stimulus number (also, append the order number (i) to the recorded data)
    $mappings[$parsed_line[0]] = $parsed_line[1] ."\t". ($i+1);
  }
  // Sorts the $mappings array by key
  ksort($mappings);
  // Implode the $mappings array, using a line break as the glue
  $new_data = implode("\n", $mappings);
  // Write the new data to the data file
  writeFile('../data/experiment_'. $condition .'/' . $chain_code .'/'. $generation.'s', $new_data);
}

// Save a test answer to a participant's dynamic or stable set file
function saveFinalCommAnswer($condition, $chain_code, $generation, $position, $answer, $xy, $sel_xy) {
  // Import the global variable $set_size
  global $set_size;
  // Parse the map position into a set type ("d" or "s") and the stimulus number
  $position = explode('.', $position);
  // Load in the lines from a specific stable set file
  $lines = loadFile($condition, $chain_code, $generation, 's');
  // Concatenate the stimulus number, answer, XY coordinates, and timestamp (delimited by tabs) for the final test item
  $answer = $position[1] .'|||'. trim($answer) ."\t". $xy[0] .','. $xy[3] ."\t". $xy[1] .','. $xy[4] ."\t". $xy[2] .','. $xy[5] ."\t". date("H:i:s") ."\t". $sel_xy[0] .','. $sel_xy[3] ."\t". $sel_xy[1] .','. $sel_xy[4] ."\t". $sel_xy[2] .','. $sel_xy[5];
  // Add the final answer to the lines array
  array_push($lines, $answer);
  // Set up an empty array in which to dump the parsed lines
  $mappings = array();
  // For each line in the file...
  for ($i=0; $i < $set_size; $i++) {
    // Parse the line into its stimulus number and recorded data
    $parsed_line = explode('|||', $lines[$i]);
    // Put the recorded data into the $mappings array with a key equal to the stimulus number (also, append the order number (i) to the recorded data)
    $mappings[$parsed_line[0]] = $parsed_line[1] ."\t". ($i+1);
  }
  // Sorts the $mappings array by key
  ksort($mappings);
  // Implode the $mappings array, using a line break as the glue
  $new_data = implode("\n", $mappings);
  // Write the new data to the data file
  writeFile('../data/experiment_'. $condition .'/' . $chain_code .'/'. $generation.'s', $new_data);
}

// Clear the data files for a specific participant
function clearFiles($condition, $chain_code, $generation) {
  // Overwrite the dynamic set file with "" (null)
  writeFile('../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation.'d', '');
  // Overwrite the stable set file with "" (null)
  writeFile('../data/experiment_'. $condition .'/'. $chain_code .'/'. $generation.'s', '');
}

function parseMap($map) {
  // Parse the map into its constituent parts
  $map = explode('||', $map);
  // Parse the first map item for information about the page and stimulus number
  $map_position = explode('-', $map[0]);
  // Remove the first item from the map
  unset($map[0]);
  // Implode the map array back to a string using double pipe as the glue
  $new_map = implode('||', $map);
  // Return the new map, and info about the page and stimulus number
  return array($new_map, $map_position[0], $map_position[1]);
}

?>
