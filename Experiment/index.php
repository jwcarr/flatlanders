<?php

include("globals.php");
include("php/file.php");

// If a specific page has been specified, set that as the current page; otherwise, goto the parameters page
if ($_REQUEST["page"] != "") { $page = $_REQUEST["page"]; } else { $page = "parameters"; }

// If we are currently in the experiment...
if ($page == "experiment") {
  include("php/triangle.php");
  include("php/main.php");
}

?>
<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Infinity</title>
<link rel="stylesheet" type="text/css" href="css/stylesheet.css" />
<script src='js/jquery.js'></script>

<?php

if ($page == "experiment" AND $experiment_page == "BREAK") {
  echo "<script src='js/countdown.js' type='text/javascript'></script>";
}

include("js/functions.js");

?>

</head>
<body<?php echo $js_onload; ?>>

<?php

if ($set_size % $mini_test_frequency != 0) { echo "WARNING: Global parameter mini_test_frequency must be a divisor of set_size"; }

if ($page == "parameters") {
  include("html/parameters.html");
}

elseif ($page == "validation") {
  include("html/validation.html");
}

elseif ($page == "experiment") {

  if ($experiment_page == "BEGIN") {
    include("html/welcome.html");
  }

  elseif ($experiment_page == "TR") {
    include("html/training.html");
  }

  elseif ($experiment_page == "MT") {
    include("html/mini_test.html");
  }

  elseif ($experiment_page == "TS") {
    include("html/test.html");
  }

  elseif ($experiment_page == "TA") {
    include("html/test_array.html");
  }

  elseif ($experiment_page == "BREAK") {
    include("html/break.html");
  }

  elseif ($experiment_page == "WAIT") {
    include("html/wait.html");
  }

  elseif ($experiment_page == "END") {
    include("html/end.html");
  }

  else {
    echo "<h1>Map error</h1><p>Please inform the experiment supervisor.</p>";
  }

}

else {
  echo "<h1>Page error</h1><p>Please inform the experiment supervisor.</p>";
}

?>

</body>
</html>
