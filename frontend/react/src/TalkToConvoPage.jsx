import React, { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import styled from 'styled-components';

const CONSTS = {
    container_background_color: "rgba(0,0,0,.03)",
    container_border_color: "rgba(0,0,0,.125)",
    padding: '10px',
    grid_gap: '2rem',
};

const synth = window.speechSynthesis;
synth.cancel();

const Styles = styled.div`
    .experiment-container {
        height: calc(100vh - 17rem);
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        grid-template-rows: 130px repeat(4, 1fr);
        grid-column-gap: ${CONSTS.grid_gap};
        grid-row-gap: ${CONSTS.grid_gap};
        margin-top: 40px;
    }

    .voice-text-container {
        grid-column-start: 1;
        grid-column-end: 6;
        grid-row-start: 1;
        grid-row-end: 6;
        display: grid;
        grid-template-rows: 80% 10% 10%;
        border: 1px solid ${CONSTS.container_border_color};
        background-color: ${CONSTS.container_background_color};
        border-radius: 0.25rem;
        padding: 10px;
    }

    .input-container,
    .voice-input-container {
        display: flex;
        align-items: center;
    }

    .conversation-container {
        display: flex;
        flex-direction: column;
    }

    .conversation {
        overflow: auto;
        height: fit-content;
        margin-top: auto;
    }
    
    .textbox {
        width: -webkit-fill-available;
        margin-left: ${CONSTS.padding};
        margin-right: ${CONSTS.padding};
        height: 38px;
    }

    .btn-textbox {
        margin-left: auto;
        display: flex;
        margin-right: ${CONSTS.padding};
    }
    
    .user-utter {
        text-align: right;
        width: 100%;
        padding-bottom: ${CONSTS.padding};
    }
    
    .agent-utter {
        text-align: left;
        width: 100%;
        padding-bottom: ${CONSTS.padding};
    }
    
    .user-utter > div {
        display: inline-block;
        border-radius: 20px;
        border: 1px solid #bee5eb;
        background-color: #d1ecf1;
        color: #0c5460;
        padding: ${CONSTS.padding};
        margin-right: 10px;
        margin-left: 10px;
    }
    
    .agent-utter > div {
        display: inline-block;
        border-radius: 20px;
        background-color: white;
        padding: ${CONSTS.padding};
        margin-left: 10px;
        margin-right: 10px;
    }

    .microphone {
        margin: auto;
    }
    
    .microphone button {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid black;
        text-decoration: none;
        display: flex;
        flex-direction: row;
        align-items: center;
        margin: 0 auto;
    }
    
    .microphone button:focus {
        outline: none;
    }

    .recording-status {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        border: 1px solid black;
        margin-left: 10px;
    }
    
    .recording-status-recording {
        background: red;
        border: none;
    }

`;

const TalkToConvoPage = (props) => {
    const [state, setState] = useState('home');
    const [userMessage, setUserMessage] = useState("");
    const [chatMessages, setChatMessages] = useState([]); // list of chat messages with the label of either convo or the user

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
            console.log('inside speak message');
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
                        setState(data.state);
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
      }, [props.socketFlask]
    );

    useEffect(() => {
        document.querySelector('.conversation').scrollTop = document.querySelector('.conversation').scrollHeight;
      }
    );

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
    
    const submitMessage = (message, speak) => {
        let messageToAdd = {'text': message, 'className': 'user-utter', 'speak': speak};
        setChatMessages(chatMessages => [...chatMessages, messageToAdd]);
        handleSubmit(message, speak);
    }
    
    const handleSubmit = (message, speak) => {
        if (state === "executing" && message.toLowerCase().trim() === "stop")
            synth.cancel();
        props.socketFlask.emit('message', {
            message: message,
            sid: props.sid,
            speak: speak,
            isUnconstrained: true,
        })
    };

    const renderChatBox = () => {

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
                        <Button variant="light" className="btn-record">
                            <div>Hold Spacebar to Talk</div>
                            <div className="recording-status"></div>
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

    return (
        <Styles>
            <div className="experiment-container">
                {renderChatBox()}
            </div>
        </Styles>
    )

}

export default TalkToConvoPage;
