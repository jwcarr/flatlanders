<!DOCTYPE HTML>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Flatlanders Visualizer</title>
<link rel="stylesheet" type="text/css" href="stylesheet.css" />
<script src='jquery.js'></script>
</head>

<body>

<div class='header'>

  <h1>Flatlanders Visualizer</h1>

  <div class='header-menu'>

    <form action="index.php" action="post">

      <input type="hidden" name="page" value="load" />

      <p>

        Experiment:
        <select name="exp" id='exp' style="width: 90px;">
          <option value="<?php echo $_REQUEST['exp']; ?>"><?php echo $_REQUEST['exp']; ?></option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>

        &nbsp;&nbsp;&nbsp;&nbsp;

        Chain:
        <select name="chain" id='chain' style="width: 90px;">
          <option value="<?php echo $_REQUEST['chain']; ?>"><?php echo $_REQUEST['chain']; ?></option>
        </select>

        &nbsp;&nbsp;&nbsp;&nbsp;


        Generation:
        <select name="gen" id='gen' style="width: 90px;">
          <option value="<?php echo $_REQUEST['gen']; ?>"><?php echo $_REQUEST['gen']; ?></option>
        </select>

        &nbsp;&nbsp;&nbsp;&nbsp;

        Set:
        <select name="set" id='set' style="width: 90px;">
          <option value="<?php echo $_REQUEST['set']; ?>"><?php echo $_REQUEST['set']; ?></option>
          <option value="s">Stable</option>
          <option value="d">Dynamic</option>
          <option value="c">Combined</option>
        </select>

        &nbsp;&nbsp;&nbsp;&nbsp;

        <button type="submit">LOAD</button>
      </p>

    </form>

  </div>

</div>

<div class='body'>

<?php

if ($_REQUEST['page'] == 'load') {

  include('file.php');

  $participant = new Participant($_REQUEST['exp'], $_REQUEST['chain'], $_REQUEST['gen'], $_REQUEST['set']);

  include('view.html');
  include('view.js');

}

include('parameters.js')

?>

</div>

</body>

</html>
