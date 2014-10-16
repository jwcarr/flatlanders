<script>

var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>];
var next_page_location = '<?php echo $window_location; ?>';
var answer = '';

// On page load...
$( document ).ready( function() {
  DrawTriangle('rectangle', target_triangle);
  $("#testtext").focus();
});

// On loss of focus from the input box...
$( document ).on('blur', '#testtext', function() {
  $("#testtext").focus();
});

// On submit of a mini-test answer...
$( "#send_word" ).submit( function() {
  answer = $("#testtext").val()
  if (answer == "") {
    return false;
  }
  else {
    $("#testtext").prop("disabled", true);
    if (answer == '<?php echo $correct_answer; ?>') {
      document.getElementById('tink').play();
      $("#feedback").attr("src", "images/check.png");
      $("#testtext").css("color", "#67C200");
      setTimeout("SaveMTResponse()", <?php echo $mini_test_feedback_time; ?>);
    }
    else {
      document.getElementById('funk').play();
      $("#feedback").attr("src", "images/cross.png");
      $("#testtext").val("<?php echo $correct_answer; ?>");
      $("#testtext").css("color", "#FF2F00");
      $("#testtext").css("font-style", "italic");
      setTimeout("SaveMTResponse()", <?php echo $mini_test_feedback_time; ?>);
    }
    return false;
  }
});

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
