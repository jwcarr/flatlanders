<?php

// Check test question answers
if ($_REQUEST['q1'] == 4 and $_REQUEST['q2'] == 2 and $_REQUEST['q3'] == 4) {

  // Assign the rater with an available ID
  $valid_id = new File($data_directory . 'valid_id', True);
  $id = $valid_id->getLine(0);
  $valid_id->removeLine(0);
  $valid_id->overwrite();
  unset($valid_id);
  $id = $id[0];

  // Copy the data file for that ID from the 'raw_sets' directory to the 'started' directory
  copy($data_directory . 'raw_sets/' . $id, $data_directory . 'started/' . $id);

  // Initalize Rater object
  $rater = new Rater($id);

  // Validate the Rater object
  if ($rater->validate()) {

    // Get the left/right labels for this rater
    $labels = $rater->getLeftRightLabels();

  }

  else {

    // Return error if Rater object doesn't validate
    $page = 'error';
    $error = 'Error 3';

  }

}

// On failure of test questions...
else {

  // Log IP address
  $ip_log = new File($data_directory . 'ip_log', True);
  $ip_log->addLine(array($_SERVER['REMOTE_ADDR']));
  $ip_log->overwrite();
  unset($ip_log);

  // Set cookie
  setcookie('tst', 'false', time()+2419200);

  // Send rater to ineligible page
  $page = 'ineligible';

}

?>
