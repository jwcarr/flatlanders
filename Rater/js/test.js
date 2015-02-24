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

var q1 = '';
var q2 = '';
var q3 = '';

$("#next_button").click( function() {
  window.location = 'index.php?page=instructions&q1=' + q1 + '&q2=' + q2 + '&q3=' + q3;
});

$("select[id^='question']").change( function() {
  var q = $(this).attr('id').match(/question(\d)/)[1];

  if (q == 1) { q1 = $("#question1").val(); }
  else if (q == 2) { q2 = $("#question2").val(); }
  else if (q == 3) { q3 = $("#question3").val(); }

  if (q1 != "" && q2 != "" && q3 != "") {
    enableNext();
  }
});

$(document).ready( function() {
  disableNext();
});

</script>
