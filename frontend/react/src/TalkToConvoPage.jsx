import React, { useState } from 'react';
import styled from 'styled-components';
import ChatBox from './components/ChatBox';

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
        border: 1px solid ${CONSTS.container_border_color};
        text-decoration: none;
        display: flex;
        flex-direction: row;
        align-items: center;
        margin: 0 auto;
    }

    .recording-status {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        border: 1px solid ${CONSTS.container_border_color};
        margin-left: 10px;
    }
    
    .recording-status-recording {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        border: 1px solid ${CONSTS.container_border_color};
        margin-left: 10px;
        background: red;
        border: none;
    }

`;

const TalkToConvoPage = (props) => {
    const [state, setState] = useState('home');

    const callbackFunction = (childState) => {
        setState(childState);
    }

    return (
        <Styles>
            <div className="experiment-container">
                <ChatBox sid={props.sid} isUnconstrained={true} state={state} parentCallback={callbackFunction} socketNode={props.socketNode} socketFlask={props.socketFlask}/>
            </div>
        </Styles>
    )

}

export default TalkToConvoPage;
