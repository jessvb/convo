const fs = require('fs');
const path = require('path');
const vars = require('dotenv').config();
const axios = require('axios');
const express = require('express');
const app = express();
const host = '0.0.0.0';
const port = 8080;
const httpServer = require('http').Server(app);
const io = require('socket.io')(httpServer);

app.use(express.static('public'));

if (process.env.NODE_ENV && process.env.NODE_ENV === "production") {
    // Simple password protection:
    // From https://stackoverflow.com/questions/23616371/basic-http-authentication-with-node-and-express-4
    app.use((req, res, next) => {
        const auth = {
            login: 'feb4',
            password: 'letstryit!'
        };

        // parse login and password from headers
        const b64auth = (req.headers.authorization || '').split(' ')[1] || '';
        const [login, password] = new Buffer(b64auth, 'base64').toString().split(':');

        // Verify login and password are set and correct
        if (login && password && login === auth.login && password === auth.password) {
            // Access granted...
            return next();
        }

        // Access denied...
        res.set('WWW-Authenticate', 'Basic realm="401"');
        res.status(401)
            .send('Authentication required: Please enter the username and password provided by the user study administrators.');
    });
}

app.get('/', (req, res) => res.sendFile(path.resolve('public/html/home.html')));
app.get('/demographic-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/demographic-survey.html')));
app.get('/conclusion', (req, res) => res.sendFile(path.resolve('public/html/conclusion.html')));

app.get('/practice-info', (req, res) => res.sendFile(path.resolve('public/html/stage-info/practice-info.html')));
app.get('/novice-info', (req, res) => res.sendFile(path.resolve('public/html/stage-info/novice-info.html')));
app.get('/advanced-info', (req, res) => res.sendFile(path.resolve('public/html/stage-info/advanced-info.html')));

app.get('/practice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/practice-stage-text.html')));
app.get('/practice-voice', (req, res) => res.sendFile(path.resolve('public/html/stages/practice-stage-voice.html')));
app.get('/practice-voice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/practice-stage-voice-text.html')));

app.get('/novice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/novice-stage-text.html')));
app.get('/novice-voice', (req, res) => res.sendFile(path.resolve('public/html/stages/novice-stage-voice.html')));
app.get('/novice-voice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/novice-stage-voice-text.html')));

app.get('/advanced-text', (req, res) => res.sendFile(path.resolve('public/html/stages/advanced-stage-text.html')));
app.get('/advanced-voice', (req, res) => res.sendFile(path.resolve('public/html/stages/advanced-stage-voice.html')));
app.get('/advanced-voice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/advanced-stage-voice-text.html')));

app.get('/experiments', (req, res) => res.sendFile(path.resolve('public/html/experiment-templates/index.html')));
app.get('/voice-and-conversation', (req, res) => res.sendFile(path.resolve('public/html/experiment-templates/voice-and-conversation.html')));
app.get('/text-and-conversation', (req, res) => res.sendFile(path.resolve('public/html/experiment-templates/text-and-conversation.html')));
app.get('/voice-and-program', (req, res) => res.sendFile(path.resolve('public/html/experiment-templates/voice-and-program.html')));
app.get('/voice-and-text', (req, res) => res.sendFile(path.resolve('public/html/experiment-templates/voice-and-text.html')));
app.get('/voice-only', (req, res) => res.sendFile(path.resolve('public/html/experiment-templates/voice-only.html')));
app.get('/demo', (req, res) => res.sendFile(path.resolve('public/html/demo.html')));

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
        speech_contexts: [
            [
                "create a procedure",
                "create",
                "make",
                "variable",
                "class",
                "property",
                "procedure",
                "conditional",
                "while loop",
                "until loop",
                "run",
                "list",
                "add",
                "add step",
                "delete step",
                "remove step",
                "change step",
                "replace step",
                "if",
                "is greater than",
                "is less than",
                "is equal to",
                "is greater than or equal to",
                "is less than or equal to"
            ]
        ]
    },
    interimResults: false
};

streams = {};

io.on('connection', (client) => {
    let id = client.id;
    let startStream = () => {
        streams[id] = speechClient.streamingRecognize(request)
            .on('error', (err) => {
                console.log("Restarting stream.");
                console.log(err);
                io.to(`${client.id}`).emit('streamError', err);
            })
            .on('data', (data) => {
                if (data.results[0] && data.results[0].alternatives[0]) {
                    let transcript = data.results[0].alternatives[0].transcript;
                    io.to(`${client.id}`).emit('clientUtter', transcript);
                } else {
                    console.log('Reached transcription time limit, press Ctrl+C');
                }
            });
    }

    let endStream = () => {
        if (id in streams) {
            streams[id].end();
            delete streams[id];
        }
    }

    client.on('join', (data) => {
        id = data == null ? client.id : data;
        console.log(`Client ${id} connected to server.`);
        io.to(`${client.id}`).emit('joined', id);
    });

    client.on('disconnect', () => {
        console.log(`Client ${id} disconnected.`);
    });

    client.on('startStream', () => {
        console.log('Starting stream.');
        startStream();
    });

    client.on('endStream', () => {
        console.log('Ending stream.');
        endStream();
    });

    client.on('audio', (data) => {
        if (!(id in streams))
            console.log("Stream is null.")
        else if (!streams[id].writable)
            console.log("Stream became unwritable.");
        else
            streams[id].write(data);
    });
});

httpServer.listen(port, host, () => {
    console.log(`HTTP server started at http://${host}:${port}/.`)
});