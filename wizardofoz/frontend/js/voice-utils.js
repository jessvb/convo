var agentVoice;
var msg; // this is global because of a strange bug: https://stackoverflow.com/a/35935851

/**
 * Speaks with the voice set by agentVoice
 * @param {*} text: the text the agent says
 * @param {*} onSpeak: a function that's called when the agent starts speaking
 * @param {*} callback: a function that's called when the agent is done speaking
 */
function speakText(text, onSpeak, callback) {
    // FROM https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API
    msg = new SpeechSynthesisUtterance(text);

    msg.voice = agentVoice; // Note: some voices don't support altering params
    msg.volume = 1; // 0 to 1
    msg.rate = 1.1; // 0.1 to 10
    // msg.pitch = 1.5; // 0 to 2 -- Zhorai's voice is at 1.5
    msg.pitch = 1;
    msg.lang = 'en-US';

    // onSpeak e.g., set the button to the "hear again" button
    if (onSpeak) {
        onSpeak();
    }

    if (callback) {
        msg.onend = function () {
            callback();
        };
    }

    window.speechSynthesis.speak(msg);
}

/* -------------- Once the page has loaded -------------- */
document.addEventListener('DOMContentLoaded', function () {
    // Prepare the agent's voice:
    window.speechSynthesis.onvoiceschanged = function () {
        // good voices: Alex pitch 2, Google US English 1.5, Google UK English Female 1.5, Google UK English Male 2
        agentVoice = window.speechSynthesis.getVoices().filter(function (voice) {
            return voice.name == 'Google US English';
            // return voice.name == 'Google UK English Female';
            // return voice.name == 'Google UK English Male';
            // return voice.name == 'Alex';
        })[0];
    };
});