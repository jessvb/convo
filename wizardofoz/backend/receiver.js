/* to connect to website via websocket: */
var WebSocket = require('ws');
var https = require('https');
var fs = require('fs');

const port = 8082;
const server = https.createServer({
    cert: fs.readFileSync('/etc/letsencrypt/live/zhorai.csail.mit.edu/cert.pem'),
    key: fs.readFileSync('/etc/letsencrypt/live/zhorai.csail.mit.edu/privkey.pem')
});

/* to write to txt file: */
var fs = require('fs');

/* to execute bash scripts */
var exec = require('child_process').exec;

/* to read input from wizard (i.e., terminal input) */
var readline = require('readline');
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});


// Create secure websocket server
const wss = new WebSocket.Server({
    server
});

// Define websocket handlers
wss.on('connection', function (connection) {
    connection.on('message', function incoming(message) {
        // process WebSocket message
        console.log('received message: ' + message);
        var sendEnd = false;
        var jsonMsg = JSON.parse(message);
        if (jsonMsg.command == 'parse') {

        } else {
            console.log("Error: Command, '" + jsonMsg.command + "', not recognized. Closing connection.");
            sendEnd = true;
        }

        // End the ws connection if sendEnd==true
        if (sendEnd) {
            sendDone(connection);
        }
    });

    connection.on('close', function (connection) {
        // client closed connection
        console.log("Closed connection.\n");
    });

});

function returnTextToClient(text, stage, connection) {
    console.log("Returning text to client: " + JSON.stringify({
        'filedata': text,
        'stage': stage
    }));
    connection.send(
        JSON.stringify({
            'filedata': text,
            'stage': stage
        }));
    sendDone(connection);
}

function sendDone(connection) {
    // tell the client to close the connection
    connection.send(JSON.stringify({
        'done': true
    }));
}

server.listen(port);

console.log("Wizard is all set!");

rl.question('Say something: ', (answer) => {
    // TODO: Log the answer in a database
    console.log(`Okay, I'll send: ${answer}, to the frontend. (TODO)`);

    rl.close();
});