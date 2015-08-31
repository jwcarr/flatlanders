<?php

$rater = new Rater($_REQUEST['id']);

if ($rater->validate() !== False) {

  if ($rater->logStartTime() === False) {

    $page = 'error';
    $error = 'Error 5';

  }

}

else {

  $page = 'error';
  $error = 'Error 4';

}

?>
