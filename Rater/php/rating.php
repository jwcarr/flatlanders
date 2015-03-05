<?php

include_once('class.rater.php');

$rater = new Rater($_REQUEST['id']);

if ($rater->validate() !== False) {

  if (is_null($_REQUEST['rating_num']) === False) {

    if ($rater->storeRating($_REQUEST['rating_num'], $_REQUEST['triangle1'], $_REQUEST['triangle2'], $_REQUEST['rating']) === False) {

      $page = 'error';
      $error = 'Error 2';

    }

    if ($rater->getTimeTaken() < 3) {
      $rater->blockRater();
      $rater->save();
      $page = 'early_exit';
      return;
    }

  }

  $triangle_pair = $rater->getCurrentTriangles();

  if (gettype($triangle_pair) != 'array') {
    // Task is complete

    $rater->blockRater();

    // Issue completion code and set completion secret
    $completion_code = $rater->generateCompletionCode();
    $completion_secret = $triangle_pair;

    // Send to end page
    $page = 'end';

  }

  else {

    $triangle1 = $triangle_pair[0];
    $triangle2 = $triangle_pair[1];
    $triangle1_id = $triangle_pair[2];
    $triangle2_id = $triangle_pair[3];
    $labels = $rater->getLeftRightLabels();

  }

  if (is_null($_REQUEST['rating_num']) === False) {

    if ($rater->save()) {

      if ($page == 'end') {
        $id = $rater->id;
        unset($rater);
        rename('../../server_data/tst/started/' . $id, '../../server_data/tst/completed/' . $id);
      }

    }

    else {

      $page = 'error';
      $error = 'Error 6';

    }

  }

}

else {

  $page = 'error';
  $error = 'Error 1';

}

?>
