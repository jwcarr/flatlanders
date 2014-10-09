<?php

include("php/file.php");

$map = openFile("data/client");

writeFile("data/client", "");

if ($map != "" OR $map != false) {
	header("Location: index.php?".$map);
}

?>

<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Infinity</title>
<link rel="stylesheet" type="text/css" href="css/stylesheet.css" />
</head>

<body>

<div id='title'>
	Server not ready
</div>

<div id='subhead'>
	Set up the server first and <a href='client.php'>try again</a>.
</div>

</body>
</html>
