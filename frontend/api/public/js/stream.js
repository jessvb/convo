const strings_to_replace = {
    "1/2": "1 to",
    "wow": "while",
    "wild": "while",
    "pat": "pet",
    "crater": "create",
    "closed": "close",
    "trader": "create",
    "dumb": "done",
    "gun": "done"
}

const strings_to_replace_at_start = {
    "save": "say",
    "it's": "if",
    "its": "if",
    "well": "while"
}

socket.on('clientUtter', (transcript) => {
    let final = transcript.toLowerCase();
    let data = {
        'sid': localStorage.getItem('sid'),
        'stage': localStorage.getItem('currStage'),
        'part': localStorage.getItem('currPart')
    }
    for (let string in strings_to_replace) {
        if (final.includes(string)) {
            data['original'] = string;
            data['replacement'] = strings_to_replace[string];
            socketApi.emit('wordReplace', data);
            final = final.replace(string, strings_to_replace[string]);
        }
    }
    for (let string in strings_to_replace_at_start) {
        if (final.startsWith(string)) {
            data['original'] = string;
            data['replacement'] = strings_to_replace_at_start[string];
            socketApi.emit('wordReplace', data);
            final = final.replace(string, strings_to_replace_at_start[string]);
        }
    }
    submitMessage(final, true);
});

AudioContext = window.AudioContext || window.webkitAudioContext;

let btnRecord = document.getElementById("btn-record");
let status = document.getElementById("recording-status");
let experimentDiv = document.getElementById("experiment-container");

let handleKeyDown = (event) => {
    btnRecord.onmousedown = null;
    btnRecord.onmouseup = null;
    synth.cancel();
    let tag = event.target.tagName.toLowerCase();
    if (event.code == 'Space' && tag != 'input' && tag != 'textarea') { startRecording(); }
}

let handleKeyUp = (event) => {
    btnRecord.onmousedown = startRecording;
    btnRecord.onmouseup = stopRecording;
    let tag = event.target.tagName.toLowerCase();
    if (event.code == 'Space' && tag != 'input' && tag != 'textarea') { stopRecording(); }
}

btnRecord.onmousedown = () => {
    document.onkeydown = null;
    document.onkeyup = null;
    synth.cancel();
    startRecording();
}

btnRecord.onmouseup = () => {
    document.onkeydown = handleKeyDown;
    document.onkeyup = handleKeyUp;
    stopRecording();
}

document.onkeydown = handleKeyDown;
document.onkeyup = handleKeyUp;

let isRecording = false;
let isStreaming = false;

let context;
let processor;
let input;
let stream;

let startRecording = () => {
    if (isRecording)
        return;

	console.log("Starting recording.");
    status.className = "recording";
    isRecording = true;

    data = {
        "sid": localStorage.getItem("sid"),
        "part": localStorage.getItem("currPart"),
        "stage": localStorage.getItem("currStage")
    };
    socket.emit('startStream', data);
    isStreaming = true;

    context = new AudioContext();
    processor = context.createScriptProcessor(2048, 1, 1);
    processor.connect(context.destination);
    context.resume();

    let handleSuccess = (s) => {
        stream = s;
        input = context.createMediaStreamSource(stream);
        input.connect(processor);
        processor.onaudioprocess = (e) => socket.emit('audio', downsample(e.inputBuffer.getChannelData(0), 44100, 16000));
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(handleSuccess)
        .catch(console.log);
};

let stopRecording = () => {
	console.log("Stopping recording.");
    status.className = "";

    socket.emit('endStream');
    isStreaming = false;

    stream.getTracks()[0].stop();
    input.disconnect(processor);
    processor.disconnect(context.destination);
    context.close().then(() => {
        input = null;
        processor = null;
        context = null;
        isRecording = false;
    });
};

let downsample = (buffer, sampleRate, outSampleRate) => {
	if (outSampleRate == sampleRate)
		return buffer;

    if (outSampleRate > sampleRate)
		console.error("downsampling rate show be smaller than original sample rate");

    let sampleRateRatio = sampleRate / outSampleRate;
	let newLength = Math.round(buffer.length / sampleRateRatio);
	let result = new Int16Array(newLength);
	let offsetResult = 0;
    let offsetBuffer = 0;

	while (offsetResult < result.length) {
		let nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
        let accum = 0, count = 0;

		for (let i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
			accum += buffer[i];
			count++;
		}

		result[offsetResult] = Math.min(1, accum / count) * 0x7FFF;
		offsetResult++;
		offsetBuffer = nextOffsetBuffer;
    }

	return result.buffer;
}

window.onbeforeunload = () => {
	if (isStreaming || isRecording)
		socket.emit('endStream');
};
