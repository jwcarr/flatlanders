<script>

var data = <?php echo json_encode($participant->data); ?>;
var scale_factor = getScalingFactor();

var canvas_varience = document.getElementById("varience");
var context_varience = canvas_varience.getContext("2d");

var canvas_prototype = document.getElementById("prototype");
var context_prototype = canvas_prototype.getContext("2d");

if (scale_factor > 1) {
  canvas_varience.setAttribute('width', 500*scale_factor);
  canvas_varience.setAttribute('height', 500*scale_factor);
  context_varience.scale(scale_factor, scale_factor);

  canvas_prototype.setAttribute('width', 500*scale_factor);
  canvas_prototype.setAttribute('height', 500*scale_factor);
  context_prototype.scale(scale_factor, scale_factor);
}

function drawTriangles(refs) {
  for (i=0; i<refs.length; i++) {
    var sep = refs[i].split(';');
    var ref_array = sep[0].split(',');
    for (j=0; j<ref_array.length; j++) {
      drawTriangle(data[ref_array[j]], sep[1]);
    }
  }
}

function drawPrototype(refs) {
  var prototype = [0,0,0,0,0,0];
  for (i=0; i<refs.length; i++) {
    var sep = refs[i].split(';');
    var ref_array = sep[0].split(',');
    for (j=0; j<ref_array.length; j++) {
      for (k=1; k<7; k++) {
        prototype[k-1] += parseFloat(data[ref_array[j]][k]);
      }
    }
    console.log(prototype);
    for (l=0; l<6; l++) {
      prototype[l] = prototype[l] / 4;
    }
    //console.log(prototype);
    //drawTriangle(data[ref_array[0]], sep[1]);
  }
}

function drawTriangle(cords, colour) {
  context_varience.beginPath();
  context_varience.moveTo(cords[1], cords[4]);
  context_varience.lineTo(cords[2], cords[5]);
  context_varience.lineTo(cords[3], cords[6]);
  context_varience.closePath();
  context_varience.lineWidth = <?php echo $triangle_line_thickness; ?>;
  context_varience.strokeStyle = colour;
  context_varience.stroke();
  context_varience.beginPath();
  context_varience.arc(cords[1], cords[4], "<?php echo $orienting_spot_radius; ?>", 0, 2 * Math.PI, false);
  context_varience.fillStyle = colour;
  context_varience.fill();
  context_varience.lineWidth = 1;
  context_varience.strokeStyle = colour;
  context_varience.stroke();
}

function getScalingFactor() {
  if ('devicePixelRatio' in window) {
    if (window.devicePixelRatio > 1) {
      return window.devicePixelRatio;
    }
  }
  return 1;
}

$(document).on('change', '#word_select', function() {
  context_varience.clearRect(0, 0, canvas_varience.width, canvas_varience.height);
  drawTriangles($(this).val());
  //context_prototype.clearRect(0, 0, canvas_prototype.width, canvas_prototype.height);
  //drawPrototype($(this).val());
});

</script>
