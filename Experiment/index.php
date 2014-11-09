<!DOCTYPE HTML>
<head>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Infinity</title>
<link rel="stylesheet" type="text/css" href="css/stylesheet.css" />
<script src='js/jquery.js'></script>

<?php

include('globals.php');
include('php/file.php');

// If a specific page has been requested, set that as the current page; otherwise default to the parameters page
if ($_REQUEST["page"] != '') { $page = $_REQUEST['page']; } else { $page = 'parameters'; }

// If we are currently in the experiment...
if ($page == 'experiment') {
  include('php/triangle.php');
  include('php/main.php');

  // If a communnication page has been requested, add JavaScript for connecting to the node.js server
  if ($experiment_page == "DR" OR $experiment_page == "MR" OR $experiment_page == "WAIT") {
    echo '<script src="js/node_modules/socket.io/node_modules/socket.io-client/dist/socket.io.js"></script>';
  }

  // If the break page has been requested, add JavaScript for the countdown timer
  elseif ($experiment_page == 'BREAK') {
    echo '<script src="js/countdown.js"></script>';
  }

}

?>
</head>

<body>

<?php

// Include the relevant HTML and JavaScript files for the requested page
if ($page == 'experiment') {

  if ($experiment_page == 'TR') { include('html/training.html'); include('js/training.js'); }

  elseif ($experiment_page == 'MT') { include('html/mini_test.html'); include('js/mini_test.js'); }

  elseif ($experiment_page == 'TS') { include('html/test.html'); include('js/test.js'); }

  elseif ($experiment_page == 'DR') { include('html/director.html'); include('js/director.js'); }

  elseif ($experiment_page == 'MR') { include('html/matcher.html'); include('js/matcher.js'); }

  elseif ($experiment_page == 'BEGIN') { include('html/begin.html'); include('js/begin.js'); }

  elseif ($experiment_page == 'WAIT') { include('html/wait.html'); include('js/wait.js'); }

  elseif ($experiment_page == 'BREAK') { include('html/break.html'); }

  elseif ($experiment_page == 'END') { include('html/end.html'); }

  else { include('html/error.html'); }

}

elseif ($page == 'parameters') { include('html/parameters.html'); include('js/parameters.js'); }

elseif ($page == 'validation') { include('html/validation.html'); }

else { include('html/error.html'); }

?>

</body>

</html>
