<script>

var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>]

//When the testing page loads, draw the triangle, and then give focus to the response textbox
function TestingLoad() {
  DrawTriangle('rectangle', target_triangle);
  document.f.a.focus();
}

// Check that the participant has not given a blank answer
function CheckAnswer() {
  if (document.f.a.value == '') {
    return false;
  }
  document.f.a.blur();
  return true;
}

// Draw a triangle on the canvas
function DrawTriangle(canvasID, cords) {
  var canvas = document.getElementById(canvasID);
  var c = canvas.getContext('2d');
  c.beginPath();
  c.moveTo(cords[0], cords[3]);
  c.lineTo(cords[1], cords[4]);
  c.lineTo(cords[2], cords[5]);
  c.closePath();
  c.lineWidth = <?php echo $triangle_line_thickness; ?>;
  c.strokeStyle = 'black';
  c.stroke();
  c.beginPath();
  c.arc(cords[0], cords[3], "<?php echo $orienting_spot_radius; ?>", 0, 2 * Math.PI, false);
  c.fillStyle = 'black';
  c.fill();
  c.lineWidth = 1;
  c.strokeStyle = 'black';
  c.stroke();
}

// Check for duplicates in a participant's answers
function CheckDuplicates() {
  if (document.f.a.value == '') {
    return false;
  }
  var used_words = [<?php echo $overused_words; ?>];
  if (used_words.indexOf(document.f.a.value) != -1) {
    document.getElementById('instruction').innerHTML = 'Ooops! You’ve used this word too often. Please use another word.';
    document.getElementById('instruction').style.color = '#FF2F00';
    document.f.a.value = '';
    document.f.overuse.value = <?php echo $_REQUEST["overuse"]+1; ?>;
    return false;
  }
  document.f.a.blur();
  return true;
}

</script>
