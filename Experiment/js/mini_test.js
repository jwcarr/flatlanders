<script>

var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>]

// Location of the next_page_location page
var next_page_location = '<?php echo $window_location; ?>';
var answer = '';

//When the testing page loads, draw the triangle, and then give focus to the response textbox
function TestingLoad() {
  DrawTriangle('rectangle', target_triangle);
  document.f.a.focus();
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
      setTimeout("SaveMTResponse()", <?php echo $mini_test_feedback_time; ?>);
    }
    else {
      document.getElementById('funk').play();
      document.getElementById('feedback').src = 'images/cross.png';
      document.f.a.style.color = '#FF2F00';
      document.f.a.style.fontStyle = 'oblique';
      answer = document.f.a.value;
      setTimeout("SaveMTResponse()", <?php echo $mini_test_feedback_time; ?>);
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

</script>
