/* --- utils for sending text to the server --- */
var url = 'wss://zhorai.csail.mit.edu:8082';

function sendText(text) {
    sendJson({
        'text': text
    });
}

function sendJson(json) {
    var socket = new WebSocket(url);
    socket.onopen = function (event) {
        socket.send(JSON.stringify(json));
    };

    socket.onmessage = function (event) {
        onReceive(event, socket);
    };
}

function sendFromSession(key) {
    sendText(SentenceManager.getSessionData(key));
}

function onReceive(event, socket) {
    var jsonMsg = JSON.parse(event.data);
    if (jsonMsg.text) {
        console.log("received message: " + jsonMsg.text);
        var agentSpeech = jsonMsg.text;
        showAgentSpeech(agentSpeech);

        speakText(agentSpeech, null,
            function () {
                switchButtonTo('micBtn');
                document.getElementById('curr_text').style.visibility = "hidden";
                addSentenceToPage(agentSpeech, true);
            });
    } else {
        console.log("received message with no text.");
    }

    if (jsonMsg.done == true) {
        socket.close();
    }
}

// TODO: del:
// /**
//  * Parses given text and returns it with a call to onReceive.
//  * e.g., parseSession('mindmap', 'polarbear', 'parsing_mod1')
//  * or,   parseSession('mindmap', 'camel', 'parsing' + '_mod3');
//  *
//  * @param {*} typeOutput : e.g., 'Topic', 'Name', 'Dictionary', etc.
//  * @param {*} key : the key used for session storage. This will be used to retrieve
//  * the value stored (e.g., the sentences associated with the animal-key).
//  * @param {*} stage : the current zhorai stage you're in, if applicable.
//  * (This informs 'onReceive' what to do)
//  *
//  */
// function parseSession(typeOutput, key, stage) {
//     var value = SentenceManager.getSentencesAsString(key);
//     sendJson({
//         'command': 'parse',
//         'text': value,
//         'typeOutput': typeOutput, // e.g., 'Topic', 'Name', 'Mindmap', etc.
//         'stage': stage
//     });
// }