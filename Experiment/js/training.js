<script>

var next_page_location = '<?php echo $window_location; ?>';
var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>];

// On page load...
$( document ).ready( function() {
  DrawTriangle('rectangle', target_triangle);
  setTimeout("ShowWord()", <?php echo $word_delay; ?>);
  setTimeout("NextPage()", <?php echo $time_per_training_item; ?>);
});

// Send to next page
function NextPage() {
  window.location = next_page_location;
}

// Show the training item and play the vocalization
function ShowWord() {
  document.getElementById('alex').play();
  $("#message").html("<?php echo $training_word; ?>");
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
