const socket = io.connect("http://localhost:8080");

let bufferSize = 2048,
	AudioContext,
	context,
	processor,
	input,
	globalStream;


socket.on('connect', (data) => {
	socket.emit('join', 'Connected to server.');
});

socket.on('message', (data) => {
	console.log(data);
});

socket.on('transcript', (transcript) => {
	console.log(transcript);
	let div = document.createElement("div");
	div.className = 'blue pb2';
	div.innerHTML = `Client: ${transcript}`;
	document.getElementById("chat-container").appendChild(div);
});

socket.on('response', (response) => {
	console.log(response);
	let div = document.createElement("div");
	div.className = 'purple pb2';
	div.innerHTML = `Rasa: ${response}`;
	document.getElementById("chat-container").appendChild(div);
})

let isRecording = false;
let isStreaming = false;

var startButton = document.getElementById("start-record-btn");
startButton.onclick = e => startRecording();
startButton.disabled = false;

var stopButton = document.getElementById("stop-record-btn");
stopButton.onclick = e => stopRecording();
stopButton.disabled = true;

let startRecording = () => {
	if (isRecording){
		return;
	}

	console.log("Starting recording.");
	isRecording = true;
	startButton.disabled = true;
	stopButton.disabled = false;

	socket.emit('startStream');
	isStreaming = true;

	AudioContext = window.AudioContext || window.webkitAudioContext;
	context = new AudioContext({ latencyHint: 'interactive', });
	processor = context.createScriptProcessor(bufferSize, 1, 1);
	processor.connect(context.destination);
	context.resume();

	var handleSuccess = (stream) => {
		globalStream = stream;
		input = context.createMediaStreamSource(stream);
		input.connect(processor);
		processor.onaudioprocess = (e) => microphoneProcess(e);
	};

	if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ audio: true })
			.then(handleSuccess)
			.catch((err) => {
				console.log(err);
			});
	}
}

let microphoneProcess = (e) => {
	var left = e.inputBuffer.getChannelData(0);
	let left16 = convertFloat32ToInt16(left);
	socket.emit('audio', left16);
}

let stopRecording = () => {
	console.log("Stopping recording.");
	stopButton.disabled = true;
	socket.emit('endStream');
	isStreaming = false;

	let track = globalStream.getTracks()[0];
	track.stop();

	input.disconnect(processor);
	processor.disconnect(context.destination);
	context.close().then(() => {
		input = null;
		processor = null;
		context = null;
		AudioContext = null;
		startButton.disabled = false;
		isRecording = false;
	});
}

let convertFloat32ToInt16 = (buffer) => {
    let l = buffer.length;
    let buf = new Int16Array(l / 3);

    while (l--) {
        if (l % 3 === 0) {
            buf[l / 3] = buffer[l] * 0xFFFF;
        }
    }
    return buf.buffer
}

window.onbeforeunload = () => {
	if (isStreaming) {
		socket.emit('endStream');
	}
};
