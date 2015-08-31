<script>

var triangle1 = <?php echo json_encode($triangle1); ?>;
var triangle2 = <?php echo json_encode($triangle2); ?>;
var percent_complete = ((<?php echo $rater->current; ?> / 136) * 100).toFixed(1) + '%';
var slider_moved = false;
var min_time_elapsed = false;
var canvas1 = document.getElementById("canvas1");
var context1 = canvas1.getContext("2d");
var canvas2 = document.getElementById("canvas2");
var context2 = canvas2.getContext("2d");
var rating = null;

function drawTriangle(triangle, context) {
  context.beginPath();
  context.moveTo(triangle[0][0], triangle[0][1]);
  context.lineTo(triangle[1][0], triangle[1][1]);
  context.lineTo(triangle[2][0], triangle[2][1]);
  context.closePath();
  context.lineWidth = 2;
  context.strokeStyle = 'black';
  context.stroke();
  context.beginPath();
  context.arc(triangle[0][0], triangle[0][1], 8, 0, 2 * Math.PI, false);
  context.fillStyle = 'black';
  context.fill();
  context.lineWidth = 1;
  context.strokeStyle = 'black';
  context.stroke();
}

function submitRating() {
    window.location.replace('index.php?page=rating&id=<?php echo $rater->id; ?>&rating_num=<?php echo $rater->current; ?>&triangle1=<?php echo $triangle1_id; ?>&triangle2=<?php echo $triangle2_id; ?>&rating=' + rating);
}

function timeElapsed() {
  min_time_elapsed = true;
  if (slider_moved == true) {
    pressEnter();
  }
}

function pressEnter() {
  $("#next_box").html('Press enter to submit rating...');
}

$(document).ready( function() {
  drawTriangle(triangle1, context1);
  drawTriangle(triangle2, context2);
  $("#next_box").html('Progress: ' + percent_complete);
  setTimeout("timeElapsed()", 3000);
});

$(document).keypress( function(event) {
  if (slider_moved == true && min_time_elapsed == true) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') {
      rating = $("#rating_slider").val();
      if ($.isNumeric(rating) == false) {
        alert('Invalid rating. Please check the slider.');
      }
      else {
        $("#next_box").html('');
        $("#canvas_area").html('<button id="submit_button" class="purple" onclick="submitRating()">NEXT</button>');
        $("#slider_area").html('');
      }
    }
  }
});

$("#rating_slider").change( function() {
  slider_moved = true;
  if (min_time_elapsed == true) {
    pressEnter();
  }
});

</script>
