// Establish connection with the Node server
var socket = io.connect( 'http://' + server_ip + ':' + node_port );

////////////////////////////////////////////////////////////////////////////////////////////////
// TRANSMISSION - EVENT EMITTERS
////////////////////////////////////////////////////////////////////////////////////////////////

// On submit of the ready button...
$( "#ready" ).submit( function() {
	socket.emit( 'ready', { name: s } );
	document.getElementById("message").innerHTML = "<img src='images/loading.gif' width='33' height='33' />";
	$("#instruction").html( "Waiting for your partner..." );
	return false;
});

// On submit of a test answer...
$( "#send_word" ).submit( function() {
	var w = $("#testtext").val();
	if (w != "") {
		var c = target_triangle;
		socket.emit( 'word', { name: s, word: w, coordinates: c } );
		document.getElementById("message").innerHTML = "<img src='images/loading.gif' width='33' height='33' />";
		$("#instruction").html( "Waiting for your partner’s response..." );
	}
	return false;
});

// On click of a triangle from the matcher array...
$( "canvas[id^='match']" ).click( function() {
	if (position >= 0) {
		var resp_id = "#" + $(this).attr('id');
		var resp = resp_id.match(/#match(\d+)/)[1];
		if (resp == position) {
			var corr = true;
			$(resp_id).css({"border": "solid #3B6C9D 1px", "background-color": "#E6ECF3"});
		}
		else {
			var corr = false;
			var targ_id = "#match" + position;
			$(targ_id).css({"border": "solid #3B6C9D 1px", "background-color": "#E6ECF3"});
		}
		position = -1;
		cord = triangles.slice(resp*6, (resp*6)+6);
		socket.emit( 'feedback', { name: s, correct: corr, coordinates: cord } );
		setTimeout('NextPage()' , feedback_time);
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
		$("#message").html( data.word );
		$("#instruction").html( "Which triangle is your partner seeing?" );
		DrawTriangleArray(data.coordinates);
	}
});

// On reception of a 'feedback' transmission from the Node server...
socket.on( 'feedback', function( data ) {
	if (data.name != s) {
		var cord = data.coordinates;
		var corr = data.correct;
		$("#instruction").html( "Please wait..." );
		$("#target-stim-container").css("float", "left")
		$("#stim-label" ).html( "your triangle" );
		$("#stimuli-container").append("<div id='feedback-stim-container'><div id='feedback-stim'><canvas id='feedback_box' width='" + canvas_width + "' height='" + canvas_height + "' style='border: solid #3B6C9D 1px; background-color: #E6ECF3;'></canvas></div><div id='stim-label'>partner’s selection</div></div>");
		DrawTriangle("feedback_box", cord);

		setTimeout('NextPage()' , feedback_time);
	}
});
