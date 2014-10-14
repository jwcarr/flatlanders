<script>

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

// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

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
      var percentage_score = ((score / trials) * 100).toFixed(1);
      $("#score").html("Score: " + percentage_score + "%")
    }
    position = -1;
    cord = triangles.slice(resp*6, (resp*6)+6);
    socket.emit( 'feedback', { name: s, correct: corr, coordinates: cord } );
    setTimeout('NextPage()' , feedback_time);
  }
});

// On reception of a 'word' transmission from the Node server...
socket.on( 'word', function( data ) {
  if (data.name != s) {
    $("#message").html( data.word );
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
