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
