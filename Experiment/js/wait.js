<script>

var next_page_location = '<?php echo $window_location; ?>';
var server_ip = '<?php echo $server_ip; ?>';
var node_port = '<?php echo $node_port; ?>';
var s = "<?php echo $_REQUEST['subject']; ?>";

// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

// On submit of the ready button...
$( "#ready" ).submit( function() {
  socket.emit( 'ready', { name: s } );
  $("#message").html("<img src='images/loading.gif' width='33' height='33' />");
  $("#instruction").html("Waiting for your partner...");
  return false;
});

// On reception of a 'start' transmission from the Node server...
socket.on( 'start', function( ) {
  window.location = next_page_location + "&trials=0&score=0";
});

</script>
