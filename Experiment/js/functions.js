<script type="text/javascript">

// Location of the next_page_location page
var next_page_location = '<?php echo $window_location; ?>';
var answer = '';
var server_ip = '<?php echo $server_ip; ?>';
var node_port = '<?php echo $node_port; ?>';
var feedback_time = "<?php echo $feedback_time; ?>";
var s = "<?php echo $_REQUEST['subject']; ?>";
var array_size = <?php echo $triangle_array_size[0]*$triangle_array_size[1]; ?>;
var canvas_width = <?php echo $canvas_size[0]; ?>;
var canvas_height = <?php echo $canvas_size[1]; ?>;

// Send to next page
function NextPage() {
  window.location = next_page_location;
}

// Show the training item and play the vocalization
function ShowWord() {
  document.getElementById('alex').play();
  $("#message").html("<?php echo $training_word; ?>");
}

// Applies to welcome page only. On pressing the 'enter key', move to the next page
function KeyCheck() {
  var keyID = event.keyCode;
  if (keyID == 13) {
    window.location = next_page_location + '&first_training_item=yes';
  }
}

var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>]

// When the training page loads, draw the triangle, set delay for showing the training item, and set delay for moving to next page
function TrainingLoad() {
  DrawTriangle('rectangle', target_triangle);
  setTimeout("ShowWord()", <?php echo $word_delay; ?>);
  setTimeout("NextPage()", <?php echo $time_per_training_item; ?>);
}

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

// Give feedback on whether the participant got the mini test right or wrong
function GiveFeedback() {
  if (document.f.a.value == '') {
    return false;
  }
  else {
    document.f.a.blur();
    if (document.f.a.value == '<?php echo $correct_answer; ?>') {
      document.getElementById('tink').play();
      document.getElementById('feedback').src = 'images/check.png';
      document.f.a.style.color = '<?php if($colourblind==True){echo "#008CED";} else {echo"#67C200";} ?>';
      answer = document.f.a.value;
      setTimeout("SaveMTResponse()", <?php echo $feedback_time; ?>);
    }
    else {
      document.getElementById('funk').play();
      document.getElementById('feedback').src = 'images/cross.png';
      document.f.a.style.color = '#FF2F00';
      document.f.a.style.fontStyle = 'oblique';
      answer = document.f.a.value;
      setTimeout("SaveMTResponse()", <?php echo $feedback_time; ?>);
      document.f.a.value = '<?php echo $correct_answer; ?>';
    }
    return false;
  }
}

// Send to next page, saving the mini test answer
function SaveMTResponse() {
  window.location = next_page_location + '&a=' + answer + '&correct_answer=<?php echo $correct_answer; ?>';
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

var triangles = [];
var position = -1;

function DrawTriangleArray(target_coordinates) {
  var distractor_triangles = [<?php echo $triangle_array_JS; ?>];
  position = Math.floor(Math.random()*array_size);
  triangles = distractor_triangles.slice( 0, position*6 ).concat( target_coordinates ).concat( distractor_triangles.slice( position*6 ) );

  n = <?php echo $triangle_array_size[1]*$triangle_array_size[0]; ?>;

  for (i=0; i<(n*6); i+=6) {
    DrawTriangle('match'+(i/6), [triangles[i], triangles[i+1], triangles[i+2], triangles[i+3], triangles[i+4], triangles[i+5]]);
  }
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
