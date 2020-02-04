document.addEventListener('DOMContentLoaded', (event) => {
    // generate / store an id for the computer / browser in local storage
    getUniqueId();

    // set the button url
    let button = document.getElementById('btn-begin');
    button.onclick = () => { window.location.href = "/demographic-survey"; };
});

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
