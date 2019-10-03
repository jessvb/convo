const fs = require('fs');
const path = require('path');
const vars = require('dotenv').config();

const express = require('express');
const app = express();
const port = 8080;
const host = '0.0.0.0';
const rasa_host = process.env.RASA_HOSTNAME || "localhost";
const server = require('http').Server(app);
const io = require('socket.io')(server);
const rasaSocket = require('socket.io-client')(`http://${rasa_host}:5005`);

app.use('/public', express.static(path.join(__dirname, 'public')));

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/index.html');
});

const speech = require('@google-cloud/speech');
const speechClient = new speech.SpeechClient();

const encoding = 'LINEAR16';
const sampleRateHertz = 16000;
const languageCode = 'en-US';

const request = {
    config: {
        encoding: encoding,
        sampleRateHertz: sampleRateHertz,
        languageCode: languageCode,
    },
    interimResults: false
};

rasaSocket.on('connect', () => {
    console.log("Connected to Rasa server.");
});

rasaSocket.on('disconnect', () => {
    console.log("Disconnected from Rasa server.");
});

rasaSocket.on('rasaResponse', data => {
    io.emit("response", data["text"]);
})

io.on('connection', (client) => {
    let recognizeStream = null;
    console.log('Client connected to server.');

    client.on('join', (data) => {
        client.emit('message', 'Socket connected to server.');
    });

    client.on('startStream', () => {
        console.log('Starting stream.');
        startRecognizeStream(client);
    });

    client.on('endStream', () => {
        console.log('Ending stream.');
        endRecognizeStream();
    });

    client.on('audio', function (data) {
        if (recognizeStream !== null) {
            recognizeStream.write(data);
        }
    });

    let startRecognizeStream = (client) => {
        recognizeStream = speechClient.streamingRecognize(request)
            .on('error', console.error)
            .on('data', (data) => {
                if (data.results[0] && data.results[0].alternatives[0]) {
                    let transcript = data.results[0].alternatives[0].transcript;
                    console.log(data.results[0].alternatives[0].transcript);
                    client.emit('transcript', transcript);
                    rasaSocket.emit('rasaInput', { "message": transcript });
                } else {
                    console.log('Reached transcription time limit, press Ctrl+C');
                }
            }
        );
    }

    function endRecognizeStream() {
        if (recognizeStream) {
            recognizeStream.end();
        }

        recognizeStream = null;
    }
});

server.listen(port, host, () => {
    console.log(`Server started at ${host}:${port}.`)
});
