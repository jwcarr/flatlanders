<?php

include_once('class.rater.php');

$rater = new Rater($_REQUEST['id']);

if ($rater->validate() !== False) {

  if (is_null($_REQUEST['rating_num']) === False) {

    if ($rater->storeRating($_REQUEST['rating_num'], $_REQUEST['triangle1'], $_REQUEST['triangle2'], $_REQUEST['rating']) === False) {

      $page = 'error';
      $error = 'Error 2';

    }

    if ($_REQUEST['triangle1'] == $_REQUEST['triangle2']) {

      if ($rater->submitted_rating > 50) {
        $rater->blockRater();
        $rater->save();
        $page = 'early_exit';
        return;
      }

    }

    if ($rater->getTimeTaken() < 3) {
      $rater->blockRater();
      $rater->save();
      $page = 'early_exit';
      return;
    }

  }

  $triangle_pair = $rater->getCurrentTriangles();

  if ($triangle_pair === False) {
    // Task is complete

    $rater->blockRater();

    // Issue completion code
    $completion_code = $rater->generateCompletionCode();

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
        rename('data/started/' . $id, 'data/completed/' . $id);
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