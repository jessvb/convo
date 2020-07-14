// Connect to servers on production
//const socket = io.connect("https://userstudy.appinventor.mit.edu");
//const socketApi = io.connect("https://userstudy.appinventor.mit.edu", { path: '/api/socket.io' })
// Connect to servers on local
const socket = io.connect('http://localhost:8080');
const socketApi = io.connect('http://localhost:5000');

// Genrates or remembers a somewhat-unique ID with distilled user-agent info.
let getUniqueId = () => {
    if (!('sid' in localStorage)) {
        let browser = findFirstString(navigator.userAgent, [
            'Seamonkey', 'Firefox', 'Chromium', 'Chrome', 'Safari', 'OPR', 'Opera',
            'Edge', 'MSIE', 'Blink', 'Webkit', 'Gecko', 'Trident', 'Mozilla'
        ]);
        let os = findFirstString(navigator.userAgent, [
            'Android', 'iOS', 'Symbian', 'Blackberry', 'Windows Phone',
            'Windows', 'OS X', 'Linux', 'iOS', 'CrOS'
        ]).replace(/ /g, '_');
        let unique = ('' + Math.random()).substr(2);
        localStorage.setItem('sid', `${os}_${browser}_${unique}`);
    }

    return localStorage.getItem('sid');
};

// Parse user agent string by looking for recognized substring.
let findFirstString = (str, choices) => {
    for (let j = 0; j < choices.length; j++) {
        if (str.indexOf(choices[j]) >= 0) {
            return choices[j];
        }
    }
    return '0';
};

socketApi.on('connect', (data) => {
    socketApi.emit('join', {
        "sid": getUniqueId(),
        "stage": localStorage.getItem("currStage"),
        "part": localStorage.getItem("currPart")
    });
});

socketApi.on('joined', (data) => {
    console.log("Socket connected to API server.");
    console.log(`SID returned from API server: ${data}`);
});

socket.on('connect', (data) => {
    socket.emit('join', {
        "sid": getUniqueId(),
        "stage": localStorage.getItem("currStage"),
        "part": localStorage.getItem("currPart")
    });
});

socket.on('joined', (data) => {
    console.log("Socket connected to Voice server.");
    console.log(`SID returned from Voice server: ${data}`);
});

socket.on('streamError', (err) => {
    console.log(err);
});
