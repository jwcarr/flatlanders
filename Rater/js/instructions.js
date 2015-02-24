<script>

function enableNext() {
  $("#next_button").prop("disabled", false);
  $("#next_button").css("background-color", "white");
  $("#next_button").css("border", "solid 3px white");
  $("#next_button").css("cursor", "pointer");
}

function disableNext() {
    $("#next_button").prop("disabled", true);
    $("#next_button").css("background-color", "#6C69D1");
    $("#next_button").css("border", "solid 3px #6C69D1");
}

$("#next_button").click( function() {
  window.location = 'index.php?page=selection&id=<?php echo $id; ?>';
});

$(document).ready( function() {
  disableNext();
  setTimeout("enableNext()", 30000);
});

</script>
