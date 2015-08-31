<?php

// GLOBALS
$canvas_size = array(500, 500);
$triangle_line_thickness = 2;
$orienting_spot_radius = 8;
$colours = array('#A0522D', '#CD5C5C', '#F08080', '#FA8072', '#E9967A',
'#DC143C', '#FF0000', '#A52A2A', '#B22222', '#8B4513', '#8B0000', '#DEB887',
'#A9A9A9', '#FFC0CB', '#FF69B4', '#FF1493', '#C71585', '#DB7093', '#FFDEAD',
'#FFA07A', '#F4A460', '#FF7F50', '#FF6347', '#D2691E', '#FF4500', '#CD853F',
'#FF8C00', '#FFF8DC', '#FFD700', '#DAA520', '#FFFF00', '#FFEFD5', '#FFE4B5',
'#FFEBCD', '#FFDAB9', '#EEE8AA', '#F0E68C', '#BDB76B', '#B8860B', '#E6E6FA',
'#D8BFD8', '#DDA0DD', '#EE82EE', '#DA70D6', '#FF00FF', '#BA55D3', '#9370DB',
'#9966CC', '#8A2BE2', '#9932CC', '#8B008B', '#4B0082', '#BC8F8F', '#6A5ACD',
'#483D8B', '#D2B48C', '#ADFF2F', '#7FFF00', '#00FF00', '#32CD32', '#90EE90',
'#00FA9A', '#00FF7F', '#2E8B57', '#228B22', '#008000', '#006400', '#9ACD32',
'#F5DEB3', '#6B8E23', '#808000', '#556B2F', '#66CDAA', '#8FBC8F', '#20B2AA',
'#008B8B', '#2F4F4F', '#00FFFF', '#000000', '#AFEEEE', '#7FFFD4', '#48D1CC',
'#5F9EA0', '#4682B4', '#B0C4DE', '#ADD8E6', '#87CEEB', '#00BFFF', '#1E90FF',
'#6495ED', '#7B68EE', '#4169E1', '#0000CD', '#191970', '#708090', '#696969');

class Participant {

  public function __construct($experiment, $chain, $generation, $set) {
    $this->data = $this->loadFile($experiment, $chain, $generation, $set);
  }

  public function getWordOptions() {
    global $colours;
    $unique_words = array();
    for ($i=0; $i<48; $i++) {
      $datum = $this->data[$i];
      $unique_words[$datum[0]][] = $i;
    }
    ksort($unique_words);
    $c = 0;
    $d = floor(96/count($unique_words));
    foreach ($unique_words as $word=>$refs) {
      $html .= '<option value="'. implode(',', $refs) . ';' . $colours[$c] .'">'. $word .'</option>';
      $c += $d;
    }
    return $html;
  }

  // Load the file for a given participant's dynamic or stable set
  private function loadFile($experiment, $chain, $generation, $set) {
    // Get the data from that file
    $data = $this->openFile('../Data/'. $experiment .'/'. $chain .'/'. $generation . $set);
    // Separate the raw data at line breaks
    $lines = explode("\n", $data);
    // Set up an empty array in which to dump the words
    $data = array();
    // For each line in the data file...
    $c = 0;
    foreach ($lines as $line) {
      // Separate out the columns delimited by tabs
      $columns = explode("\t", $line);
      // Extract the XY coordinates for point A
      $xy1 = explode(',', $columns[1]);
      // Extract the XY coordinates for point B
      $xy2 = explode(',', $columns[2]);
      // Extract the XY coordinates for point C
      $xy3 = explode(',', $columns[3]);
      // Dump the first column (the word) into the $words array
      array_push($data, array($columns[0], $xy1[0], $xy2[0], $xy3[0], $xy1[1], $xy2[1], $xy3[1]));
      $c++;
    }
    // Return the lines as an array
    return $data;
  }

  // Open a file
  private function openFile($filename) {
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

}

?>
