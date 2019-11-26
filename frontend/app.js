const fs = require('fs');
const path = require('path');
const vars = require('dotenv').config();
const axios = require('axios');

const express = require('express');
const app = express();
const port = 8080;
const host = '0.0.0.0';
const server = require('http').Server(app);
const io = require('socket.io')(server);

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.resolve('public/html/home.html'));
});

app.get('/survey', (req, res) => {
    res.sendFile(path.resolve('public/html/survey.html'));
});

app.get('/practice', (req, res) => {
    res.sendFile(path.resolve('public/html/practice.html'));
});

app.get('/experiments', (req, res) => {
    res.sendFile(path.resolve('public/html/experiments/index.html'));
});

app.get('/voice-and-conversation', (req, res) => {
    res.sendFile(path.resolve('public/html/experiments/voice-and-conversation.html'));
})

app.get('/text-and-conversation', (req, res) => {
    res.sendFile(path.resolve('public/html/experiments/text-and-conversation.html'));
})

app.get('/voice-and-program', (req, res) => {
    res.sendFile(path.resolve('public/html/experiments/voice-and-program.html'));
})

app.get('/voice-and-text', (req, res) => {
    res.sendFile(path.resolve('public/html/experiments/voice-and-text.html'));
})

app.get('/voice-only', (req, res) => {
    res.sendFile(path.resolve('public/html/experiments/voice-only.html'));
})

app.get('/code', (req, res) => {
    res.sendFile(path.resolve('public/html/demo.html'));
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
                    axios.post('http://127.0.0.1:5000/message', { "message": transcript })
                        .then((res) => {
                            console.log(res);
                            client.emit('response', res.data.message);
                        })
                        .catch((err) => {
                            console.log(err);
                        })
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
