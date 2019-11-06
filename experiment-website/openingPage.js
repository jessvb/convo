// This file initializes variables in the first page of the experiment for use
// later


document.addEventListener('DOMContentLoaded', function(event) {
  // generate / store an id for the computer / browser in local storage
  getUniqueId();
  // initialize userID in local storage. This will increment if you use the same
  // computer / browser
  if (localStorage.getItem('userID') == null) {
    localStorage.setItem('userID', 0);
  }
  let userID = parseInt(localStorage.getItem('userID')) + 1;
  localStorage.setItem('userID', userID);

  // Initialize a value that is used for the progress bar.
  // Set the 'value of a survey' (note that the value of a single test is 1)
  localStorage.setItem('surveyVal', 5);

  // set the button url
  let url = 'openingSurvey.html?userID=' + userID;
  let btn = document.getElementById('begin');
  btn.addEventListener('click', function() {
    window.location.href = url;
  });
});


// Genrates or remembers a somewhat-unique ID with distilled user-agent info.
function getUniqueId() {
  if (!('uid' in localStorage)) {
    var browser = findFirstString(navigator.userAgent, [
      'Seamonkey', 'Firefox', 'Chromium', 'Chrome', 'Safari', 'OPR', 'Opera',
      'Edge', 'MSIE', 'Blink', 'Webkit', 'Gecko', 'Trident', 'Mozilla'
    ]);
    var os = findFirstString(navigator.userAgent, [
               'Android', 'iOS', 'Symbian', 'Blackberry', 'Windows Phone',
               'Windows', 'OS X', 'Linux', 'iOS', 'CrOS'
             ]).replace(/ /g, '_');
    var unique = ('' + Math.random()).substr(2);
    localStorage['uid'] = os + '-' + browser + '-' + unique;
  }
  return localStorage['uid'];
}

// Parse user agent string by looking for recognized substring.
function findFirstString(str, choices) {
    for (var j = 0; j < choices.length; j++) {
      if (str.indexOf(choices[j]) >= 0) {
        return choices[j];
      }
    }
    return '?';
  }