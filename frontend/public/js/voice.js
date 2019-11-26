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
	document.getElementById("client").innerHTML = `Client: ${transcript}`;
})

socket.on('response', (response) => {
	document.getElementById("agent").innerHTML = `Agent: ${response}`;
})

let isRecording = false;
let isStreaming = false;

var recordButton = document.getElementById("record-btn");
recordButton.onmousedown = () => startRecording();
recordButton.onmouseup = () => stopRecording();

let startRecording = () => {
	if (isRecording){
		return;
	}

	console.log("Starting recording.");
	isRecording = true;

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
		processor.onaudioprocess = (e) => socket.emit('audio', convertFloat32ToInt16(e.inputBuffer.getChannelData(0)));
	};

	if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ audio: true })
			.then(handleSuccess)
			.catch((err) => {
				console.log(err);
			});
	}
}

let stopRecording = () => {
	console.log("Stopping recording.");
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
