const fs = require('fs');
const path = require('path');
const express = require('express');
const app = express();
const host = '0.0.0.0';
const port = 8080;
const httpServer = require('http').Server(app);
const io = require('socket.io')(httpServer);
const wav = require('wav');
require('dotenv').config();
var cors = require("cors");
app.use(cors());

app.use(express.static("public"));

if (process.env.NODE_ENV && process.env.NODE_ENV === 'production') {
    // Simple password protection:
    // From https://stackoverflow.com/questions/23616371/basic-http-authentication-with-node-and-express-4
    app.use((req, res, next) => {
        const auth = {
            login: 'admin',
            password: 'appinv'
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

app.get('/debug', (req, res) => res.sendFile(path.resolve('public/html/debug.html')));

const speech = require('@google-cloud/speech');
const { debug } = require('console');
const speechClient = new speech.SpeechClient();
const encoding = 'LINEAR16';
const sampleRateHertz = 16000;
const languageCode = 'en-US';
const request = {
    'config': {
        'encoding': encoding,
        'sampleRateHertz': sampleRateHertz,
        'languageCode': languageCode,
        'speechContexts' : [
            {'phrases': ['done', 'close loop', 'while', 'create a', 'called', 'step', 'say'], 'boost': 15 },
            {'phrases': ['create a procedure', 'create a variable', 'make a variable', 'get user input', 'save it as']},
            {'phrases': ['is greater than', 'is less than', 'is equal to', 'is greater than or equal to']},
            {'phrases': ['pet', 'horse', 'cat', 'dog', 'cricket', 'bird', 'cow'], 'boost': 10},
            {'phrases': [
                'get user input and save it as pet',
                'if the value of pet',
                'run pet sounds',
                'add one to',
                'subtract one from',
                'hello world'
            ]},
            {'phrases': ['add step', 'change step', 'remove step']}
        ],
        'model': 'command_and_search'
    },
    'interimResults': false
};

let checkUserStudy = (stage, part) => {
    if (part !== 'voice-text' && part !== 'voice')
        return false;

    if (!['practice', 'novice', 'advanced'].includes(stage))
        return false;

    return true;
}

streams = {};
writers = {};

io.on('connection', (client) => {
    // Check socket connection to react server
    client.emit('reactconnection', null);

    let sessionId = client.id;
    let sid;
    let stage;
    let part;
    let startStream = () => {
        streams[sessionId] = speechClient.streamingRecognize(request)
            .on('error', (err) => {
                console.log(`[${sid}] Error occured so restarting stream.`);
                console.log(err);
                io.to(`${sessionId}`).emit('streamError', err);
            })
            .on('data', (data) => {
                if (data.results[0] && data.results[0].alternatives[0]) {
                    let transcript = data.results[0].alternatives[0].transcript;
                    io.to(`${sessionId}`).emit('clientUtter', transcript);
                } else {
                    console.log(`[${sid}] Reached transcription time limit, press Ctrl+C`);
                }
            });
    }

    let endStream = () => {
        if (sessionId in writers) {
            writers[sessionId].end();
            delete writers[sessionId];
        }
        if (sessionId in streams) {
            streams[sessionId].end();
            delete streams[sessionId];
        }
    }

    client.on('join', (data) => {
        if (data) {
            sid = data.sid;
            stage = data.stage;
            part = data.part;
            console.log(`[${sid}][${stage},${part}] Client connected to server.`);
            if (checkUserStudy(stage, part)) {
                let dir = `audio/${stage}/${part.replace('-', '_')}/${sid}`;
                fs.mkdirSync(dir, { recursive: true });
            }
            io.to(`${sessionId}`).emit('joined', sid);
        } else {
            console.log('Client connected without an SID.');
        }
    });

    client.on('disconnect', () => {
        console.log(`[${sid}][${stage},${part}] Client disconnected.`);
    });

    client.on('startStream', (data) => {
        console.log(`[${data.sid}][${data.stage},${data.part}] Starting stream.`);
        if ('sid' in data && 'part' in data && 'stage' in data) {
            if (checkUserStudy(data.stage, data.part)) {
                let audioName = `audio/${data.stage}/${data.part.replace('-', '_')}/${data.sid}/${Date.now()}.wav`;
                writers[sessionId] = new wav.FileWriter(audioName, {
                    channels: 1,
                    sampleRate: 16000,
                    bitDepth: 16,
                });
            }
        }

        startStream();
    });

    client.on('endStream', () => {
        console.log(`[${sid}][${stage},${part}] Ending stream.`);
        endStream();
    });

    client.on('audio', (data) => {
        if (!(sessionId in streams))
            console.log(`[${sid}][${stage},${part}] Stream is null.`)
        else if (!streams[sessionId].writable)
            console.log(`[${sid}][${stage},${part}] Stream became unwritable.`);
        else {
            streams[sessionId].write(data);
        }

        if (sessionId in writers)
            writers[sessionId].write(data);
    });
});

httpServer.listen(port, host, () => {
    console.log(`HTTP server started at http://${host}:${port}/.`)
});
