import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Button } from 'react-bootstrap';

const synth = window.speechSynthesis;
synth.cancel();
 
const ChatBox = (props) => {
    const [isRecording, setIsRecording] = useState(false);
    const [userMessage, setUserMessage] = useState("");
    // list of chat messages with the label of either convo or the user, have messages persist
    const [chatMessages, setChatMessages] = useState(localStorage.getItem(props.pageId) ? JSON.parse(localStorage.getItem(props.pageId)) : []);

    let context = useRef(null);
    let processor = useRef(null);
    let input = useRef(null);
    let stream = useRef(null);

    const handleSubmit = useCallback((message, speak) => {
        if (props.state === "executing" && message.toLowerCase().trim() === "stop")
            synth.cancel();
        props.socketFlask.emit('message', {
            message: message,
            sid: props.sid,
            speak: speak,
            isUnconstrained: props.isUnconstrained
        })
    }, [props.sid, props.socketFlask, props.state, props.isUnconstrained]);

    const submitMessage = useCallback((message, speak) => {
        let messageToAdd = {'text': message, 'className': 'user-utter', 'speak': speak};
        setChatMessages(chatMessages => [...chatMessages, messageToAdd]);
        handleSubmit(message, speak);
    }, [handleSubmit]);

    useEffect(() => {
        addAudioPlayer();
        const addMessage = (text, className, speak = true) => {
            if (className === "agent-utter" && speak === true) {
                speakMessage(text);
            }
            let messageToAdd = {'text': text, 'className': className, 'speak': speak};
            setChatMessages(chatMessages => [...chatMessages, messageToAdd]);
        }
    
        const speakMessage = (message) => {
            let audio = new SpeechSynthesisUtterance(message);
            audio.voice = synth.getVoices().filter((voice) => {
                return voice.name === 'Google US English' || voice.name === 'Samantha';
            })[0];
            audio.volume = 1;
            audio.rate = 0.9;
            audio.pitch = 1.0;
            audio.lang = 'en-US';
            synth.speak(audio);
        }
        
        props.socketFlask.on('response', (data) => {
            const handleSocketFlaskResponse = (data) => {
                let audioPlayer = document.getElementById('audio-player');
                if (audioPlayer.src && !audioPlayer.ended) {
                    setTimeout(() => handleSocketFlaskResponse(data), 500);
                } else {
                    if ('state' in data)
                        props.parentCallback(data.state);
                    addMessage(data.message, "agent-utter", data.speak);
                }
            }
            handleSocketFlaskResponse(data);
        });

        props.socketFlask.on('playSound', (data) => {
            const handlePlaySound = (data) => {
                let audioPlayer = document.getElementById('audio-player');
                if (audioPlayer.src && !audioPlayer.ended) {
                    setTimeout(() => handlePlaySound(data), 500);
                } else {
                    audioPlayer.src = `/sounds/${data.sound}.mp3`;
                    addMessage(`Playing ${data.sound} sound.`, "agent-utter", false);
                    const audioPromise = audioPlayer.play();
                    if (audioPromise !== undefined) {
                        audioPromise
                        .then(_ => {
                            // autoplay starts here
                        })
                        .catch(err => {
                            console.info(err);
                        });
                    }
                }
            }
            handlePlaySound(data);
        });

        return function cleanup() {
            props.socketFlask.removeAllListeners('response');
            props.socketFlask.removeAllListeners('playSound');
          };

      }, [props]
    );

    useEffect(() => {
        props.socketNode.on('clientUtter', (transcript) => {
            let final = transcript.toLowerCase();
            submitMessage(final, true);
        });

        return function cleanup() {
            props.socketNode.removeAllListeners('clientUtter');
          };

        }, [props.socketNode, submitMessage]
    );

    const startRecording = useCallback(() => {
        synth.cancel();
        if (isRecording)
            return;

        console.log("Starting recording.");
        setIsRecording(true);

        let data = {
            "sid": localStorage.getItem("sid"),
            "part": localStorage.getItem("currPart"),
            "stage": localStorage.getItem("currStage")
        };
        props.socketNode.emit('startStream', data);

        context.current = new AudioContext();
        processor.current = context.current.createScriptProcessor(2048, 1, 1);
        processor.current.connect(context.current.destination);
        context.current.resume();

        let handleSuccess = (s) => {
            stream.current = s;
            input.current = context.current.createMediaStreamSource(stream.current);
            input.current.connect(processor.current);
            processor.current.onaudioprocess = (e) => props.socketNode.emit('audio', downsample(e.inputBuffer.getChannelData(0), 44100, 16000));
        }

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(handleSuccess)
            .catch(console.log);
    }, [isRecording, props.socketNode]);

    const stopRecording = useCallback(() => {
        console.log("Stopping recording.");
        setIsRecording(false);

        props.socketNode.emit('endStream');

        stream.current.getTracks()[0].stop();
        input.current.disconnect(processor.current);
        processor.current.disconnect(context.current.destination);
        context.current.close().then(() => {
            input.current = null;
            processor.current = null;
            context.current = null;
            setIsRecording(false);
        });
    }, [props.socketNode]);

    useEffect(() => {
        const handleKeyDown = (event) => {
            let tag = event.target.tagName.toLowerCase();
            if (event.code === 'Space' && tag !== 'input' && tag !== 'textarea') { startRecording(); }
        }
    
        const handleKeyUp = (event) => {
            let tag = event.target.tagName.toLowerCase();
            if (event.code === 'Space' && tag !== 'input' && tag !== 'textarea') { stopRecording(); }
        }

        document.addEventListener("keydown", handleKeyDown);
        document.addEventListener("keyup", handleKeyUp);

        return function cleanup() {
            document.removeEventListener("keydown", handleKeyDown);
            document.removeEventListener("keyup", handleKeyUp)
        }
    }, [isRecording, props.socketNode, startRecording, stopRecording]);

    useEffect(() => {
        localStorage.setItem(props.pageId, JSON.stringify(chatMessages));
    }, [chatMessages, props.pageId]);

    useEffect(() => {
        document.querySelector('.conversation').scrollTop = document.querySelector('.conversation').scrollHeight;
      }
    );   

    let downsample = (buffer, sampleRate, outSampleRate) => {
        if (outSampleRate === sampleRate)
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

    const addAudioPlayer = () => {
        let audioPlayer = document.createElement('audio');
        audioPlayer.id = 'audio-player';
        audioPlayer.preload = 'none';
        audioPlayer.style = "display: none";
        document.body.appendChild(audioPlayer);
    }

    const submitText = () => {
        if (userMessage !== "") {
            synth.cancel();
            submitMessage(userMessage.toLowerCase(), false);
        }
        setUserMessage("");
    }

    const renderChat = () => {
        return (
            <div className="conversation-container">
                <div className="conversation">
                    {chatMessages.map((message) => {return renderChatMessage(message.text, message.className)})}
                </div>
            </div>
        )
    }

    const renderChatMessage = (messageText, className) => {
        return (
            <div className={className}>
                <div>{messageText}</div>
            </div>
        )
    }

    const renderTextInput = () => {
        return (
            <div className="input-container">
                <input 
                    type="text"
                    className="textbox"
                    placeholder="Type here..."
                    value={userMessage}
                    onChange={e => setUserMessage(e.target.value)}
                    onKeyPress={e => {if (e.key === "Enter") {
                        submitText();
                        }
                    }}
                />
                <Button onClick={submitText} variant="secondary" className="btn-textbox">Enter</Button>
            </div>
        )
    }

    const renderVoiceInput = () => {
        return (
            <div className="voice-input-container">
                <div className="microphone">
                    <Button variant="light" className="btn-record" onMouseDown={startRecording} onMouseUp={stopRecording}>
                        <div>Hold Spacebar to Talk</div>
                        <div className={isRecording ? "recording-status-recording" : "recording-status"}></div>
                    </Button>
                </div>
            </div>
        )
    }

    return (
            <div className="voice-text-container">
                {renderChat()}
                {renderTextInput()}
                {renderVoiceInput()}
            </div>
    )
}

export default ChatBox;