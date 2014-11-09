<script>

// Global variables
var next_page_location = '<?php echo $window_location; ?>';
var feedback_time = <?php echo $communication_feedback_time; ?>;
var canvas_width = <?php echo $canvas_size[0]; ?>;
var canvas_height = <?php echo $canvas_size[1]; ?>;
var target_triangle = <?php echo json_encode($xy); ?>;
var server_ip = '<?php echo $server_ip; ?>';
var node_port = '<?php echo $node_port; ?>';
var trials = <?php echo $_REQUEST['trials']; ?>;
var score = <?php echo $_REQUEST['score']; ?>;
var show_score = <?php echo json_encode($show_score); ?>;
var current = '<?php echo $item_info; ?>';
var s = "<?php echo $_REQUEST['subject']; ?>";
var w = ''
var cord = [];
var failsafe = 0;

// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

// On page load...
$( document ).ready( function() {
  failsafe = setTimeout("socket.emit( 'ready', { name: s } )", 9500);
  socket.emit( 'ready', { name: s } );
});

// On loss of focus from the input box...
$( document ).on('blur', '#testtext', function() {
  $("#testtext").focus();
});

// On reception of a 'start' transmission from the Node server...
socket.on( 'start', function( ) {
  clearTimeout(failsafe);
  DrawTriangle('rectangle', target_triangle);
  $("#message").fadeOut(0);
  $("#message").css("background-image", "url(images/message_box_left.png)");
  $("#message").html("<input name='a' type='text' value='' id='testtext' autocomplete='off' size='27' maxlength='20' />");
  $("#message").fadeIn(350);
  $("#instruction").html("Type in the word for this triangle and press Enter");
  $("#testtext").focus();
});

// On submit of a test answer...
$( "#send_word" ).submit( function() {
  w = $("#testtext").val();
  if (w != "") {
    var c = target_triangle;
    socket.emit( 'word', { name: s, word: w, coordinates: c } );
    $("#message").css("background-image", "none");
    $("#stim-label").html("You called it: <strong>" + w + "</strong>");
    $("#message").html("<img src='images/loading.gif' width='33' height='33' />");
    $("#instruction").html( "Waiting for your partner’s response..." );
  }
  return false;
});

// On reception of a 'feedback' transmission from the Node server...
socket.on( 'feedback', function( data ) {
  if (data.name != s) {
    cord = data.coordinates;
    var corr = data.correct;
    if (corr == true) {
      score += 1;
      document.getElementById('tink').play();
    }
    else {
      document.getElementById('funk').play();
    }
    trials += 1;
    if (show_score == true) {
      var points = score * 10;
      $("#score").html("<img src='images/star.png' width='33' height='33' /> " + points)
    }
    $("#instruction").html( "Please wait..." );
    $("#target-stim-container").css("float", "left")
    $("#stimuli-container").append("<div id='feedback-stim-container'><div id='feedback-stim'><canvas id='feedback_box' width='" + canvas_width + "' height='" + canvas_height + "'></canvas></div><div id='stim-label'>Your partner selected</div></div>");
    DrawTriangle("feedback_box", cord);
    setTimeout('NextPage()' , feedback_time);
  }
});

// Send to next page
function NextPage() {
  window.location = next_page_location + "&trials=" + trials + "&score=" + score + "&current=" + current + "&last_x1=" + target_triangle[0] + "&last_x2=" + target_triangle[1] + "&last_x3=" + target_triangle[2] + "&last_y1=" + target_triangle[3] + "&last_y2=" + target_triangle[4] + "&last_y3=" + target_triangle[5] + "&a=" + w + "&sub=" + s + "&cord_x1=" + cord[0] + "&cord_x2=" + cord[1] + "&cord_x3=" + cord[2] + "&cord_y1=" + cord[3] + "&cord_y2=" + cord[4] + "&cord_y3=" + cord[5];
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
