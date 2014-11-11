<script>

var chain_codes = <?php echo json_encode($chain_codes); ?>;
var max_generation_number = <?php echo $max_generation_number; ?>;

$("#condition").change( function() {

  var cond = $("#condition").val();

  if (cond == '1') {
    var chains = "";
    for (i in chain_codes[0]) {
      chains += "<option value='" + chain_codes[0][i] + "'>" + chain_codes[0][i] + "</option>";
    }
    $("#chain").html(chains);
  }

  else if (cond == '2') {
    var chains = "";
    for (i in chain_codes[1]) {
      chains += "<option value='" + chain_codes[1][i] + "'>" + chain_codes[1][i] + "</option>";
    }
    $("#chain").html(chains);
  }

  else if (cond == '3') {
    var chains = "";
    for (i in chain_codes[2]) {
      chains += "<option value='" + chain_codes[2][i] + "'>" + chain_codes[2][i] + "</option>";
    }
    $("#chain").html(chains);
  }

  $("#chain").prop("disabled", false);

  var gens = "";

  for (i=1; i<=max_generation_number; i++) {
    gens += "<option value='" + i + "'>" + i + "</option>";
  }

  $("#gen").html(gens);
  $("#gen").prop("disabled", false);

});

</script>
