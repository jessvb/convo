import React, { useEffect, useState } from 'react';
import { Button, Container, Spinner } from 'react-bootstrap';
import IntentCard from './components/IntentCard';
import styled from 'styled-components';

const Styles = styled.div`
    .intent-page {
        display: flex;
        flex-direction: row;
        overflow: auto;
        white-space: nowrap;
        padding: 25px;
        max-width: fit-content;
    }

    .add-more {
        height: 318px;
        width: 273px;
        display: flex;
        flex-direction: row;
        padding: 0px;
        cursor: pointer; 
    }

    .add-more-intents-button {
        display: flex;
        width: 240px;
        background: #FFFFFF;
        border: 1px solid #C2C2C2;
    }

    .add-more-button {
        display: inline-block;
        margin: auto;
        font-size: 1.5em;
        color: grey;
    }

    .sidebar {
        width: 33px;
        margin-left: auto;
        border: 1px solid #C2C2C2;
        background: #FBFBFB;
    }
`;

const CreateIntentPage = props => {
    const [intentId, setIntentId] = useState(localStorage.getItem("intentIndex") ? JSON.parse(localStorage.getItem("intentIndex")) : 1); // keep a unique id for each intent card
    const [intents, setIntents] = useState(localStorage.getItem("intents") ? JSON.parse(localStorage.getItem("intents")) : ["intent0", "intent1"]);
    const [isTraining, setIsTraining] = useState(false);
    const [finishedTraining, setFinishedTraining] = useState(false); // stays true if finished training even once
    const [rasaPort, setRasaPort] = useState(localStorage.getItem("rasaPort") ? JSON.parse(localStorage.getItem("rasaPort")) : "");

    useEffect(() => {
            props.socketFlask.on('trained', () => {
                setIsTraining(false);
                setFinishedTraining(true);
            });
        }, [props.socketFlask]
    );

    useEffect(() => {
        localStorage.setItem("intentIndex", JSON.stringify(intentId));
        localStorage.setItem("intents", JSON.stringify(intents));
        localStorage.setItem("rasaPort", rasaPort);
    }, [intentId, intents, rasaPort]);

    const handleAddMoreIntents = () => {
        var oneMoreIntentId = intentId + 1;
        var newIntentId = 'intent' + oneMoreIntentId.toString();
        setIntentId(oneMoreIntentId);
        let oneMoreIntent = intents.concat([newIntentId])
        setIntents(oneMoreIntent);
    };

    const renderIntentCardAddMoreButton = () => {
        return (
            <Container className="add-more" onClick={handleAddMoreIntents}>
                <div className="add-more-intents-button">
                    <div className="add-more-button">⊕</div>
                </div>
                <div className="sidebar"></div>
            </Container>
        );
    };

    const formatTrainingData = (intentPhrases) => {
        let formattedPhrase = "";
        for (var i = 0; i < intentPhrases.length; i++) {
            let intentPhrase = intentPhrases[i].value;
            formattedPhrase += intentPhrase;
            if (i !== intentPhrases.length - 1) {
                formattedPhrase += ",";
            }
        }
        return formattedPhrase;
    }

    const handleTrain = () => {
        let intentElements = document.getElementsByName("intent");
        let intents = [];
        let phrases = [];
        for (var i=0; i < intentElements.length; i++) {
            let intent = intentElements[i].value;
            if (intent !== "") {
                intents.push(intent);
                let phraseElements = document.getElementsByName(intent);
                phrases.push(formatTrainingData(phraseElements));
            }
        }

        if (intents !== []) {
            props.socketFlask.emit('train', {
                sid: localStorage.getItem('sid'),
                intents: intents,
                trainingData: phrases,
            });
        }
        setIsTraining(true);
    }
    
    const handleRasaPortChange = (e) => {
        setRasaPort(e.target.value);
    }

    const handleRasaPortSubmit = () => {
        props.socketFlask.emit('rasaPort', {
            sid: localStorage.getItem('sid'),
            port: rasaPort,
        });
    }

    const renderRasaPort = () => {
        return (
            <div style={{ padding: 25, }}>
                <label style={{ fontWeight: 700 }}>
                    Group ID:
                    <input 
                        style={{ marginLeft: 8 }}
                        type="text"
                        name="rasa-port"
                        value={rasaPort}
                        onChange={e => handleRasaPortChange(e)}
                    />
                </label>
                <Button 
                    variant="info"
                    onClick={handleRasaPortSubmit}
                    style={{ marginLeft: 8 }}>
                    Submit
                </Button>
            </div>
        )
    }

    const renderTrainButton = () => {
        return (
            <div style={{ paddingLeft: 25, alignItems: "center", display: "flex" }}>
                <Button 
                    variant="info"
                    onClick={handleTrain}
                    style={{ marginRight: 8 }}>
                    Train!
                </Button>
                { isTraining && <Spinner animation="border" variant="info" /> }
                { finishedTraining && !isTraining && <div>Done!</div> }
            </div>
        )
    }

    return (     
        <Styles>
            <div className="intent-page">
                {intents.map((intentId) => (<IntentCard intentId={intentId} />))}
                {renderIntentCardAddMoreButton()}
            </div>
            {renderRasaPort()}
            {renderTrainButton()}
        </Styles>
    )
}

export default CreateIntentPage;