<script>

// Global variables
var next_page_location = '<?php echo $window_location; ?>';
var server_ip = '<?php echo $server_ip; ?>';
var node_port = '<?php echo $node_port; ?>';
var feedback_time = "<?php echo $communication_feedback_time; ?>";
var s = "<?php echo $_REQUEST['subject']; ?>";
var array_size = <?php echo $triangle_array_size[0]*$triangle_array_size[1]; ?>;
var triangles = [];
var position = -1;
var trials = <?php echo $_REQUEST['trials']; ?>;
var score = <?php echo $_REQUEST['score']; ?>;
var show_score = <?php echo json_encode($show_score); ?>;
var failsafe = 0;

// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

// On page load...
$( document ).ready( function() {
  failsafe = setTimeout("socket.emit( 'ready', { name: s } )", 11500);
  socket.emit( 'ready', { name: s } );
});

// On click of a triangle from the matcher array...
$( "canvas[id^='match']" ).click( function() {
  if (position >= 0) {
    var resp_id = "#" + $(this).attr('id');
    var resp = resp_id.match(/#match(\d+)/)[1];
    if (resp == position) {
      var corr = true;
      score += 1;
      document.getElementById('tink').play();
      $(resp_id).css({"border": "solid #3B6C9D 1px", "background-color": "#E6ECF3"});
      $(resp_id).fadeIn(75).fadeOut(75).fadeIn(75).fadeOut(75).fadeIn(75).fadeOut(75).fadeIn(75).fadeOut(75).fadeIn(75);
    }
    else {
      var corr = false;
      document.getElementById('funk').play();
      $(resp_id).css({"border": "solid black 1px", "background-color": "#EFEFEF"});
      var targ_id = "#match" + position;
      $(targ_id).css({"border": "solid #3B6C9D 1px", "background-color": "#E6ECF3"});
      $(targ_id).fadeIn(75).fadeOut(75).fadeIn(75).fadeOut(75).fadeIn(75).fadeOut(75).fadeIn(75).fadeOut(75).fadeIn(75);
    }
    trials += 1;
    if (show_score == true) {
      var points = score * 10;
      $("#score").html("<img src='images/star.png' width='33' height='33' /> " + points)
    }
    position = -1;
    cord = triangles.slice(resp*6, (resp*6)+6);
    socket.emit( 'feedback', { name: s, correct: corr, coordinates: cord } );
    $("#instruction").html("Please wait...");
    setTimeout('NextPage()' , feedback_time);
  }
});

socket.on( 'start', function( ) {
  clearTimeout(failsafe);
});

// On reception of a 'word' transmission from the Node server...
socket.on( 'word', function( data ) {
  if (data.name != s) {
    $("#message").fadeOut(0);
    $("#message").css("background-image", "url(images/message_box_right.png)");
    $("#message").html( data.word );
    $("#message").fadeIn(350);
    $("#instruction").html( "Which triangle is your partner seeing?" );
    DrawTriangleArray(data.coordinates);
  }
});

// Send to next page
function NextPage() {
  window.location = next_page_location + "&trials=" + trials + "&score=" + score;
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

// Draw all the distractor triangles + the target triangle (in a random position) on the matcher array
function DrawTriangleArray(target_coordinates) {
  var distractor_triangles = [<?php echo $triangle_array_JS; ?>];
  position = Math.floor(Math.random()*array_size);
  triangles = distractor_triangles.slice(0, position*6).concat(target_coordinates).concat(distractor_triangles.slice(position*6));
  n = <?php echo $triangle_array_size[1]*$triangle_array_size[0]; ?>;
  for (i=0; i<(n*6); i+=6) {
    DrawTriangle('match'+(i/6), triangles.slice(i, i+6));
  }
}

</script>
