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
app.get('/conclusion', (req, res) => res.sendFile(path.resolve('public/html/conclusion.html')));

// Surveys:
app.get('/demographic-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/demographic-survey.html')));
app.get('/novice-text-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/stage-survey-template.html')));
app.get('/novice-voice-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/stage-survey-template.html')));
app.get('/novice-voice-text-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/stage-survey-template.html')));
app.get('/advanced-text-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/stage-survey-template.html')));
app.get('/advanced-voice-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/stage-survey-template.html')));
app.get('/advanced-voice-text-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/stage-survey-template.html')));
app.get('/comparison-survey', (req, res) => res.sendFile(path.resolve('public/html/surveys/comparison-survey.html')));

// Information pages:
app.get('/practice-info', (req, res) => res.sendFile(path.resolve('public/html/stage-info/practice-info.html')));
app.get('/novice-info', (req, res) => res.sendFile(path.resolve('public/html/stage-info/novice-info.html')));
app.get('/advanced-info', (req, res) => res.sendFile(path.resolve('public/html/stage-info/advanced-info.html')));

// Practice stage parts:
app.get('/practice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/practice-stage-text.html')));
app.get('/practice-voice', (req, res) => res.sendFile(path.resolve('public/html/stages/practice-stage-voice.html')));
app.get('/practice-voice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/practice-stage-voice-text.html')));

// Novice stage parts:
app.get('/novice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/novice-stage-text.html')));
app.get('/novice-voice', (req, res) => res.sendFile(path.resolve('public/html/stages/novice-stage-voice.html')));
app.get('/novice-voice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/novice-stage-voice-text.html')));

// Advanced stage parts:
app.get('/advanced-text', (req, res) => res.sendFile(path.resolve('public/html/stages/advanced-stage-text.html')));
app.get('/advanced-voice', (req, res) => res.sendFile(path.resolve('public/html/stages/advanced-stage-voice.html')));
app.get('/advanced-voice-text', (req, res) => res.sendFile(path.resolve('public/html/stages/advanced-stage-voice-text.html')));

// Various test pages:
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
                "create a procedure", "create", "make",
                "variable", "class", "property", "procedure",
                "conditional", "while", "until", "close loop",
                "run", "add", "add step", "delete step", "remove step", "change step", "replace step",
                "if", "is", "greater than", "less than", "equal to", "greater than or equal to", "less than or equal to",
                "pet", "horse", "cat", "dog", "cricket", "bird", "cow"
            ]
        ]
    },
    interimResults: false
};

streams = {};

io.on('connection', (client) => {
    let sessionId = client.id;
    let sid;

    let startStream = () => {
        streams[sessionId] = speechClient.streamingRecognize(request)
            .on('error', (err) => {
                console.log(`[${id}] Error occured so restarting stream.`);
                console.log(err);
                io.to(`${sessionId}`).emit('streamError', err);
            })
            .on('data', (data) => {
                if (data.results[0] && data.results[0].alternatives[0]) {
                    let transcript = data.results[0].alternatives[0].transcript;
                    io.to(`${sessionId}`).emit('clientUtter', transcript);
                } else {
                    console.log(`[${id}] Reached transcription time limit, press Ctrl+C`);
                }
            });
    }

    let endStream = () => {
        if (sessionId in streams) {
            streams[sessionId].end();
            delete streams[sessionId];
        }
    }

    client.on('join', (data) => {
        if (data) {
            sid = data;
            console.log(`[${sid}] Client connected to server.`);
            io.to(`${sessionId}`).emit('joined', sid);
        } else {
            console.log('Client connected without an SID.');
        }
    });

    client.on('disconnect', () => {
        console.log(`[${sid}] Client disconnected.`);
    });

    client.on('startStream', () => {
        console.log(`[${sid}] Starting stream.`);
        startStream();
    });

    client.on('endStream', () => {
        console.log(`[${sid}] Ending stream.`);
        endStream();
    });

    client.on('audio', (data) => {
        if (!(id in streams))
            console.log(`[${sid}] Stream is null.`)
        else if (!streams[id].writable)
            console.log(`[${sid}] Stream became unwritable.`);
        else
            streams[sid].write(data);
    });
});

httpServer.listen(port, host, () => {
    console.log(`HTTP server started at http://${host}:${port}/.`)
});
