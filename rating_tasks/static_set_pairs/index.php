<?php

$data_directory = 'data/';

include_once('php/class.rater.php');

$ip_log = new File($data_directory . 'ip_log', False);

if (isset($_COOKIE['tst']) or in_array($_SERVER['REMOTE_ADDR'], $ip_log->data)) {

  $page = 'ineligible';

}

else {

  if (is_null($_REQUEST['page'])) { $page = 'test'; } else { $page = $_REQUEST['page']; }
  if ($page == 'rating') { include('php/rating.php'); }
  elseif ($page == 'selection') { include('php/selection.php'); }
  elseif ($page == 'instructions') { include('php/instructions.php'); }

}

unset($ip_log);

?>
<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Triangle similarity task</title>
<link rel="stylesheet" type="text/css" href="css/stylesheet.css" />
<script src='js/jquery.js'></script>
</head>
<body>

<div class="header">

  <div class="title">
    Triangle similarity task
  </div>

  <div id="next_box" class="next_box">
    <?php if ($page == 'instructions' or $page == 'selection' or $page == 'test') { echo '<button id="next_button">NEXT</button>'; } ?>
  </div>

</div>

<div class='body'>

<?php

if ($page == 'instructions') { include('html/instructions.html'); include('js/instructions.js'); }
elseif ($page == 'test') { include('html/test.html'); include('js/test.js'); }
elseif ($page == 'selection') { include('html/selection.html'); include('js/selection.js'); }
elseif ($page == 'rating') { include('html/rating.html'); include('js/rating.js'); }
elseif ($page == 'end') { include('html/end.html'); }
elseif ($page == 'ineligible') { include('html/ineligible.html'); }
elseif ($page == 'early_exit') { include('html/early_exit.html'); }
else { include('html/error.html'); }

?>

</div>

</body>
</html>
