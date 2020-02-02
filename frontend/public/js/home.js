document.addEventListener('DOMContentLoaded', (event) => {
    // generate / store an id for the computer / browser in local storage
    getUniqueId();

    // initialize userID in local storage. This will increment if you use the same
    // computer / browser
    if (localStorage.getItem('userID') == null) {
        localStorage.setItem('userID', 0);
    }
    let userID = parseInt(localStorage.getItem('userID')) + 1;
    localStorage.setItem('userID', userID);

    // set the button url
    let url = 'demographic-survey';
    let button = document.getElementById('btn-begin');
    button.onclick = () => {
        window.open(url, '_self');
    };
});

// Genrates or remembers a somewhat-unique ID with distilled user-agent info.
let getUniqueId = () => {
    if (!('uid' in localStorage)) {
        let browser = findFirstString(navigator.userAgent, [
            'Seamonkey', 'Firefox', 'Chromium', 'Chrome', 'Safari', 'OPR', 'Opera',
            'Edge', 'MSIE', 'Blink', 'Webkit', 'Gecko', 'Trident', 'Mozilla'
        ]);

        let os = findFirstString(navigator.userAgent, [
            'Android', 'iOS', 'Symbian', 'Blackberry', 'Windows Phone',
            'Windows', 'OS X', 'Linux', 'iOS', 'CrOS'
        ]).replace(/ /g, '_');
        let unique = ('' + Math.random()).substr(2);

        localStorage['uid'] = `${os}-${browser}-${unique}`;
    }

    return localStorage['uid'];
};

// Parse user agent string by looking for recognized substring.
let findFirstString = (str, choices) => {
    for (let j = 0; j < choices.length; j++) {
        if (str.indexOf(choices[j]) >= 0) {
            return choices[j];
        }
    }
    return '?';
};
