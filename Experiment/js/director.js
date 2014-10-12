<script>

var next_page_location = '<?php echo $window_location; ?>';
var feedback_time = "<?php echo $communication_feedback_time; ?>";
var s = "<?php echo $_REQUEST['subject']; ?>";
var canvas_width = <?php echo $canvas_size[0]; ?>;
var canvas_height = <?php echo $canvas_size[1]; ?>;
var target_triangle = [<?php echo $xy[0] .",". $xy[1] .",". $xy[2] .",". $xy[3] .",". $xy[4] .",". $xy[5]; ?>];
var server_ip = '<?php echo $server_ip; ?>';
var node_port = '<?php echo $node_port; ?>';

// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

// On page load...
$( document ).ready( function() {
  DrawTriangle('rectangle', target_triangle);
  $("#testtext").focus();
});

// On submit of a test answer...
$( "#send_word" ).submit( function() {
  var w = $("#testtext").val();
  if (w != "") {
    var c = target_triangle;
    socket.emit( 'word', { name: s, word: w, coordinates: c } );
    $("#message").html("<img src='images/loading.gif' width='33' height='33' />");
    $("#instruction").html( "Waiting for your partner’s response..." );
  }
  return false;
});

// On reception of a 'feedback' transmission from the Node server...
socket.on( 'feedback', function( data ) {
  if (data.name != s) {
    var cord = data.coordinates;
    var corr = data.correct;
    $("#instruction").html( "Please wait..." );
    $("#target-stim-container").css("float", "left")
    $("#stim-label" ).html( "your triangle" );
    $("#stimuli-container").append("<div id='feedback-stim-container'><div id='feedback-stim'><canvas id='feedback_box' width='" + canvas_width + "' height='" + canvas_height + "' style='border: solid #3B6C9D 1px; background-color: #E6ECF3;'></canvas></div><div id='stim-label'>partner’s selection</div></div>");
    DrawTriangle("feedback_box", cord);
    setTimeout('NextPage()' , feedback_time);
  }
});

// Send to next page
function NextPage() {
  window.location = next_page_location;
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
