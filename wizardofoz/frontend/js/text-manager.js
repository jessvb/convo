/* -------------- Initialize variables -------------- */
var infoLabel;
var recordButton;
var agentSpeechBox;
var loadingImg;
var blankLoadingImg;
var currBtnIsMic = true;

/* -------------- Initialize functions -------------- */
function showAgentSpeech(text) {
    agentSpeechBox.innerHTML = '<p class="agenttext">' + text + '</p>';
}

/**
 * Returns list of english voices:
 */
function getEnglishVoices() {
    englishVoices = [];
    speechSynthesis.getVoices().forEach(function (voice) {
        if (voice.lang.includes("en")) {
            englishVoices.push(voice);
        }
    });
    return englishVoices;
}

/**
 * Switches the button to the specified button (either 'micBtn' or 'speakBtn')
 * @param {*} toButton
 */
function switchButtonTo(toButton) {
    if (toButton == 'micBtn') {
        recordButton.hidden = false;
        loadingImg.hidden = true;
        blankLoadingImg.hidden = false;
        currBtnIsMic = true;
    } else if (toButton == 'speakBtn') {
        recordButton.hidden = true;
        loadingImg.hidden = true;
        blankLoadingImg.hidden = false;
        currBtnIsMic = false;
    } else if (toButton == 'loading') {
        loadingImg.hidden = false;
        blankLoadingImg.hidden = true;
        recordButton.hidden = true;
        currBtnIsMic = false;
    } else if (toButton == 'textFileBtn') {
        loadingImg.hidden = true;
        blankLoadingImg.hidden = false;
        recordButton.hidden = true;
        currBtnIsMic = false;
    } else if (toButton == 'micAndTextFileBtn') {
        recordButton.hidden = false;
        loadingImg.hidden = true;
        blankLoadingImg.hidden = false;
        blankLoadingImg.hidden = true;
        currBtnIsMic = true;
    } else if (!toButton) {
        console.log('No button specified. Not switching button.');
    } else {
        console.error('Unknown button: ' + toButton + '. Did not switch button.');
    }
}

function afterRecording(recordedText) {
    var agentSpeech = '';
    var phrases = ["Sorry, what was that?", "Oh, pardon?", "I didn't quite understand that. Pardon?"];

    agentSpeech = chooseRandomPhrase(phrases);
    showAgentSpeech(agentSpeech);

    speakText(agentSpeech, null,
        function () {
            switchButtonTo('micBtn');
        });
}

/* -------------- Once the page has loaded -------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize variables:
    currStage = 0;
    infoLabel = document.getElementById('z_info_label');
    recordButton = document.getElementById('record_button');
    agentSpeechBox = document.getElementById('final_span');
    loadingImg = document.getElementById('loadingImg');
    blankLoadingImg = document.getElementById('blankLoadingImg');

    // Add click handlers
    setUpRecordingHandlers(recordButton, function () {
        recordButtonClick({
            callback: afterRecording,
            onClickStop: switchButtonTo,
            onClickStopParam: 'loading'
        });
    });
});