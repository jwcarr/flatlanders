// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

// Retrieve subject name (SubA or SubB) for this instance
var s = $( "#sender" ).val();

////////////////////////////////////////////////////////////////////////////////////////////////
// TRANSMISSION - EVENT EMITTERS
////////////////////////////////////////////////////////////////////////////////////////////////

// On submit of the ready button...
$( "#ready" ).submit( function() {
	socket.emit( 'ready', { name: s } );
	document.getElementById("message").innerHTML = "<img src='images/loading.gif' width='33' height='33' />";
	$( "#instruction" ).html( "Waiting for your partner..." );
	return false;
});

// On submit of a test answer...
$( "#send_word" ).submit( function() {
	var w = $( "#testtext" ).val();
	var c = $( "#coordinates" ).val();
	if (w != "") {
		socket.emit( 'word', { name: s, word: w, coordinates: c } );
		document.getElementById("message").innerHTML = "<img src='images/loading.gif' width='33' height='33' />";
		$( "#instruction" ).html( "Waiting for your partner’s response..." );
	}
	return false;
});

// On submit of a match answer...
$( "#send_feedback" ).submit( function() {
	var targ = $( "#target" ).val();
	var resp = $( "#response" ).val();
	var cord = $( "#coordinates" ).val();
	if (resp == "") { return false; }
	else {
		if (resp == targ) {
			var corr = true;
		}
		else {
			var corr = false;
		}
		socket.emit( 'feedback', { name: s, correct: corr, coordinates: cord } );
		return true;
	}
});

////////////////////////////////////////////////////////////////////////////////////////////////
// RECEPTION - EVENT LISTENERS
////////////////////////////////////////////////////////////////////////////////////////////////

// On reception of a 'sync' transmission from the Node server...
socket.on( 'sync', function( ) {
	NextPage();
});

// On reception of a 'word' transmission from the Node server...
socket.on( 'word', function( data ) {
	if (data.name != s) {
		$( "#word" ).value = data.word;
		$( "#message" ).html( data.word );
		$( "#instruction" ).html( "Which triangle is your partner trying to communicate?" );
		DrawTriangleArray(data.coordinates);
	}
});

// On reception of a 'feedback' transmission from the Node server...
socket.on( 'feedback', function( data ) {
	if (data.name != s) {
		PartnerFeedback(data.correct, data.coordinates);
	}
});
