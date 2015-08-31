<script>

var chain_codes = [['A', 'B', 'C', 'D'], ['E', 'F', 'G', 'H'], ['I', 'J', 'K', 'L']];
var max_generation_number = 10;

$("#exp").change( function() {

  var cond = $("#exp").val()-1;

  var chains = "";
  for (i in chain_codes[cond]) {
    chains += "<option value='" + chain_codes[cond][i] + "'>" + chain_codes[cond][i] + "</option>";
  }
  $("#chain").html(chains);

  var gens = "";

  for (i=0; i<=max_generation_number; i++) {
    gens += "<option value='" + i + "'>" + i + "</option>";
  }

  $("#gen").html(gens);

});

</script>
