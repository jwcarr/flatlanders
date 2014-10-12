<script>

// Location of the next_page_location page
var next_page_location = '<?php echo $window_location; ?>';

// On pressing the 'enter key', move to the next page
function KeyCheck() {
  var keyID = event.keyCode;
  if (keyID == 13) {
    window.location = next_page_location + '&first_training_item=yes';
  }
}

</script>
