/* -------------- Initialize variables -------------- */
var recordButton;
var agentSpeechBox;
var loadingImg;
var blankLoadingImg;
var currBtnIsMic = true;
var inputTextbox; // for testing without speech
var sentencesDiv; // where the list of sentences appear
var devMode = true; // set to true if you want to see the input text box

/* -------------- Initialize functions -------------- */
function showAgentSpeech(text) {
    agentSpeechBox.innerHTML = '<p id="curr_text" class="agenttext">' + text + '</p>';
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
    // Add the recorded speech to the dialog, as user text:
    addSentenceToPage(recordedText, false);


    var agentSpeech = '';
    var phrases = ["Sorry, what was that?", "Oh, pardon?", "I didn't quite understand that. Pardon?"];

    agentSpeech = chooseRandomPhrase(phrases);
    showAgentSpeech(agentSpeech);

    speakText(agentSpeech, null,
        function () {
            switchButtonTo('micBtn');
            document.getElementById('curr_text').style.visibility = "hidden";
            addSentenceToPage(agentSpeech, true);
        });
}

/**
 * Adds the text (visually) to the list of sentences on the webpage. If "isAgentText"
 * is true, then the text will look visually like it came from the agent (e.g., blue
 * text). Otherwise, it will visually look like it came from the user (e.g., green
 * text).
 * @param {*} text : the sentence to be appended to the list of sentences in the UI.
 * @param {*} isAgentText : whether the text is coming from the agent (or the user).
 */
function addSentenceToPage(text, isAgentText) {
    var textNode = document.createTextNode(text);
    var parNode = document.createElement("p");
    var className = "usertext";

    if (isAgentText) {
        className = "agenttext";
    }
    parNode.prepend(textNode);
    parNode.classList.add(className);
    sentencesDiv.prepend(parNode);
}

/* -------------- Once the page has loaded -------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize variables:
    currStage = 0;
    recordButton = document.getElementById('record_button');
    agentSpeechBox = document.getElementById('final_span');
    loadingImg = document.getElementById('loadingImg');
    blankLoadingImg = document.getElementById('blankLoadingImg');
    sentencesDiv = document.getElementById('dialog');

    // Add click handlers
    if (!devMode) {
        setUpRecordingHandlers(recordButton, function () {
            recordButtonClick({
                callback: afterRecording,
                onClickStop: switchButtonTo,
                onClickStopParam: 'loading'
            });
        });
    } else {
        // show input text box
        inputTextbox = document.getElementById('inputTextbox');
        inputSubmitbtn = document.getElementById('submitBtn');
        inputTextbox.hidden = false;
        inputSubmitbtn.hidden = false;
        // click/enter handlers
        inputSubmitbtn.addEventListener('click', function () {
            console.log(inputTextbox.value);
            afterRecording(inputTextbox.value);
            inputTextbox.value = "";
        });
        inputTextbox.addEventListener('keyup', function (event) {
            // 13 is enter
            if (event.keyCode === 13) {
                event.preventDefault();
                inputSubmitbtn.click();
            }
        });
    }
});