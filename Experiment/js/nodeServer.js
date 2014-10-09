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
		console.log( data.name + " is ready.");
		if (data.name == "SubA"){
			SubA = true;
		}
		else if (data.name == "SubB") {
			SubB = true;
		}
		if (SubA == true && SubB == true) {
			SubA = false;
			SubB = false;
			io.sockets.emit( 'sync' );
		}
	});

	client.on( 'word', function( data ) {
		console.log( 'Word received: ' + data.name + ": " + data.word + ": " + data.coordinates );
		io.sockets.emit( 'word', { name: data.name, word: data.word, coordinates: data.coordinates } );
	});

	client.on( 'feedback', function( data ) {
		console.log( 'Feedback received: ' + data.name + ": " + data.correct + ": " + data.coordinates );
		io.sockets.emit( 'feedback', { name: data.name, correct: data.correct, coordinates: data.coordinates } );
	});

});

server.listen( 8080 );
