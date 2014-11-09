var socket = require( 'socket.io' );
var express = require( 'express' );
var http = require( 'http' );
var app = express();
var server = http.createServer( app );
var io = socket.listen( server, { log: false } );

var SubA = false;
var SubB = false;

io.sockets.on( 'connection', function( client ) {

	client.on( 'ready', function( data ) {
		console.log( "Trial " + data.trial_num + "  " +data.name + " is ready.");
		if (data.name == "SubA") {
			SubA = true;
		}
		else if (data.name == "SubB") {
			SubB = true;
		}
		if (SubA == true && SubB == true) {
			SubA = false;
			SubB = false;
			io.sockets.emit( 'start' );
			console.log( "Server issued start command.");
		}
	});

	client.on( 'word', function( data ) {
		io.sockets.emit( 'word', { name: data.name, word: data.word, coordinates: data.coordinates } );
		console.log( 'Word transmitted from ' + data.name + ": " + data.word + ": " + data.coordinates );
	});

	client.on( 'feedback', function( data ) {
		io.sockets.emit( 'feedback', { name: data.name, correct: data.correct, coordinates: data.coordinates } );
		console.log( 'Feedback transmitted from ' + data.name + ": " + data.correct + ": " + data.coordinates + "\n" );
	});

});

server.listen( 8080 );

console.log( 'The node server has started successfully. Awaiting communication from the clients...' );
