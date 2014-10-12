<?php

include("php/file.php");

// Read in the client file which details all the info needed to run the experiment
$client = openFile("data/client");

// If openFile() hasn't failed and the client file isn't blank...
if ($client != false AND $client != "") {
	// Clear the client file...
	writeFile("data/client", "");
	// and redirect the client terminal to the correct position in the experiment
	header("Location: index.php?".$client);
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
