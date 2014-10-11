<?php

// Generate a random triangle stimulus
function generateTriangle() {
  // Import global parameters
  global $canvas_size, $canvas_border;
  // Choose coordinates for point A
  $x1 = rand($canvas_border+1, $canvas_size[0]-$canvas_border);
  $y1 = rand($canvas_border+1, $canvas_size[1]-$canvas_border);
  // Choose coordinates for point B
  $x2 = rand($canvas_border+1, $canvas_size[0]-$canvas_border);
  $y2 = rand($canvas_border+1, $canvas_size[1]-$canvas_border);
  // Choose coordinates for point C
  $x3 = rand($canvas_border+1, $canvas_size[0]-$canvas_border);
  $y3 = rand($canvas_border+1, $canvas_size[1]-$canvas_border);
  // Return an array containing the chosen X and Y coordinates
  return array($x1, $x2, $x3, $y1, $y2, $y3);
}

// Load the coordinates for a particular triangle stimulus from a given data file
function loadTriangle($condition, $chain_code, $generation, $stimulus_set, $stimulus_number) {
  // Load in the lines from a specific data file
  $lines = loadFile($condition, $chain_code, $generation, $stimulus_set);
  // Break the particular line we need into columns using the tab as a delimiter
  $columns = explode("\t", $lines[$stimulus_number]);
  // Extract the XY coordinates for point A
  $xy1 = explode(",", $columns[1]);
  // Extract the XY coordinates for point B
  $xy2 = explode(",", $columns[2]);
  // Extract the XY coordinates for point C
  $xy3 = explode(",", $columns[3]);
  // Return the loaded coordinates
  return array($xy1[0], $xy2[0], $xy3[0], $xy1[1], $xy2[1], $xy3[1]);
}

function generateTriangleArray() {
  global $triangle_array_size;
  $triangle_array = array();
  for ($i=0; $i<($triangle_array_size[0]*$triangle_array_size[1])-1; $i++) {
    $triangle_array[] = generateTriangle();
  }
  return $triangle_array;
}

?>
