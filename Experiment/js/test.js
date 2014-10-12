<script>

var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>];
var used_words = [<?php echo $overused_words; ?>];
var cond = <?php echo $_REQUEST["cond"]; ?>

// On page load...
$( document ).ready( function() {
  DrawTriangle('rectangle', target_triangle);
  $("#testtext").focus();
});

// On submit of a test answer...
$( "#send_word" ).submit( function() {
  if ($("#testtext").val() == "") {
    return false;
  }
  else {
    if (cond == 2 && used_words.indexOf(document.f.a.value) != -1) {
      $("#instruction").html("Ooops! You’ve used this word too often. Please use another word.");
      $("#instruction").css("color", "#FF2F00");
      $("#testtext").val("");
      $("#overuse").val(<?php echo $_REQUEST["overuse"]+1; ?>);
      return false;
    }
    $("#testtext").prop("disabled", true);
    return true;
  }
});

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
