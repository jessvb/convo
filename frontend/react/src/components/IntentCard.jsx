import React, { Component } from 'react';
import { Button, Container } from 'react-bootstrap';
import styled from 'styled-components';

const COLORS = {
    yellow: '#fffec5',
    blue: '#c7ffff',
    red: '#ffc7c7',
    green: '#c7ffc7',
    purple: '#e3c7ff',
    orange: '#ffe3c7',
};

const HEX_TO_COLOR = {
    '#fffec5': 'yellow',
    '#c7ffff': 'blue',
    '#ffc7c7': 'red',
    '#c7ffc7': 'green',
    '#e3c7ff': 'purple',
    '#ffe3c7': 'orange',
}

const HIGHLIGHT_SPAN_TAGS = 
    [`<span style="background-color: rgb(255, 254, 197);">`,
     `<span style="background-color: rgb(199, 255, 255);">`,
     `<span style="background-color: rgb(255, 199, 199);">`,
     `<span style="background-color: rgb(199, 255, 199);">`,
     `<span style="background-color: rgb(227, 199, 255);">`,
     `<span style="background-color: rgb(255, 227, 199);">`
    ];

    const ORDERED_COLORS = [COLORS.yellow, COLORS.blue, COLORS.red, COLORS.green, COLORS.purple, COLORS.orange];

const synth = window.speechSynthesis;
synth.cancel();

const Styles = styled.div`
    .card {
        color: #3d3d3d;
        max-height: 80%;
        min-height: 318px;
        width: 273px;
        border: 2px solid black;
        box-sizing: border-box;
        display: flex;
        flex-direction: row;
        padding: 0px;
        margin-right: 20px;
    }

    .expanded-card {
        width: 480px;
    }

    .intent-card {
        display: flex;
        flex-direction: column;
        width: 240px;
        padding-left: 16px;
        padding-right: 16px;
        padding-top: 10px;
        padding-bottom: 10px;
        background: #F7FFF7;
        overflow: auto;
        border-right: 1px solid black;
    }

    .intent-form {
        padding: 8px;
        display: flex;
        flex-direction: column;
    }

    .label {
        font-weight: 700;
        display: flex;
        flex-direction: column;
    }

    .label-input {
        margin-top: 8px;
    }

    .add-more-button {
        display: inline-block;
        margin-left: auto;
        margin-right: auto;
        font-size: 1.5em;
        color: black;
        cursor: pointer; 
    }

    .entities-button {
        display: flex;
        flex-direction: row;
        width: 33px;
        margin-left: auto;
    }

    .entities-button span {
        display: inline-block;
        transform: rotate(90deg);
        padding: 0px;
        position: relative;
        right: 13px;
    }

    .entities-button-style {
        border-radius: 0px;
        background: #F9F9F9 !important;
        color: black !important;
        border: 0px;
        padding: 0px;
        width: 100%;
    }

    .entities-card {
        width: 207px;
    }

    .grey-color {
        background: #F9F9F9;
    }

    .highlight-entities-button {
        border-style: solid;
        border-width: thin;
        border-radius: 25px;
        text-align: center;
        font-size: small;
        cursor: pointer;
        background: white;
    }

    .entity {
        border-style: solid;
        border-width: thin;
        padding: 8px;
        margin-bottom: 8px;
    }

    .label-input-yellow {
        margin-top: 8px;
    }

    .label-input-blue {
        margin-top: 8px;
    }

    .label-input-red {
        margin-top: 8px;
    }

    .label-input-green {
        margin-top: 8px;
    }

    .label-input-purple {
        margin-top: 8px;
    }

    .label-input-orange {
        margin-top: 8px;
    }

    .label-input-yellow::selection {
        background: ${COLORS.yellow};
    }

    .label-input-blue::selection {
        margin-top: 8px;
        background: ${COLORS.blue};
    }

    .label-input-red::selection {
        margin-top: 8px;
        background: ${COLORS.red};
    }

    .label-input-green::selection {
        margin-top: 8px;
        background: ${COLORS.green};
    }

    .label-input-purple::selection {
        margin-top: 8px;
        background: ${COLORS.purple};
    }

    .label-input-orange::selection {
        margin-top: 8px;
        background: ${COLORS.orange};
    }
`;

class IntentCard extends Component {
    constructor(props) {
        super(props);

        this.state = {
            intent: localStorage.getItem(this.props.intentId) ? JSON.parse(localStorage.getItem(this.props.intentId)) : '',
            phrases: localStorage.getItem(this.props.intentId + "phrases") ? JSON.parse(localStorage.getItem(this.props.intentId + "phrases")) : [''],
            entities: localStorage.getItem(this.props.intentId + "entities") ? JSON.parse(localStorage.getItem(this.props.intentId + "entities")) : [''],
            showEntities: false,
            highlightColor: '',
            highlightColorClass: 'label-input',
            isHighlighting: false
        };
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.intent !== this.state.intent) {
            localStorage.setItem(this.props.intentId, JSON.stringify(this.state.intent));
        }
        if (prevState.phrases !== this.state.phrases) {
            localStorage.setItem(this.props.intentId + "phrases", JSON.stringify(this.state.phrases));
        }
        if (prevState.entities !== this.state.entities) {
            localStorage.setItem(this.props.intentId + "entities", JSON.stringify(this.state.entities));
        }
    }

    toggleShowEntities = () => {
        this.setState(state => ({ showEntities: !state.showEntities }));
    };

    handleAddMorePhrases = () => {
        let morePhrases = this.state.phrases.concat([''])
        this.setState({ phrases: morePhrases });
    };

    handleAddMoreEntities = () => {
        let moreEntities = this.state.entities.concat([''])
        this.setState({ entities: moreEntities });
    }

    handleIntentChange = e => {
        this.setState({ intent: e.target.value });
    }

    handleEntityChange = (e, idx) => {
        let newEntities = this.state.entities.slice();
        newEntities[idx] = e.target.value;
        this.setState({ entities: newEntities });
    }

    handlePhraseChange = (e, idx) => {
        let newPhrases = this.state.phrases.slice();
        newPhrases[idx] = e.target.value;
        this.setState({ phrases: newPhrases });
    }

    turnOnHighlighting = (color) => {
        let color_name = HEX_TO_COLOR[color];
        this.setState({ 
            highlightColorClass: `label-input-${color_name}`,
            highlightColor: color,
            isHighlighting: true });
    }

    doneHighlighting = () => {
        this.rewriteIntentPhrases();
        this.setState({
            isHighlighting: false
        });
    }

    clearHighlighting = () => {
        let selectedText = '';
        if (window.getSelection) {
            selectedText = window.getSelection();
        }
        else if (document.getSelection) {
            selectedText = document.getSelection();
        }
        else if (document.selection) {
            selectedText = document.selection.createRange().text;
        }
        selectedText.removeAllRanges();
    }

    mouseUp = () => {
        if (this.state.isHighlighting) {
            let selectedText = '';
            if (window.getSelection) {
                selectedText = window.getSelection();
            }
            else if (document.getSelection) {
                selectedText = document.getSelection();
            }
            if (selectedText.toString().length > 0) {
                // wrap the selected text in a 'highlight' the same color as the entity
                let span = document.createElement("span");
                span.style.backgroundColor = this.state.highlightColor;
                if (selectedText.rangeCount) {
                    let range = selectedText.getRangeAt(0).cloneRange();
                    // make sure there's no overlap with a previous highlight
                    if (range.toString().indexOf("<span") === -1 && range.toString().indexOf("</span>") === -1) {
                        try {
                            range.surroundContents(span);
                            selectedText.removeAllRanges();
                            selectedText.addRange(range);
                        } catch (err) {
                            console.log("not a valid highlight");
                        }
                    }
                }
            }
        }
    }

    rewriteIntentPhrases = () => {
        let newPhrases = [];
        let phraseElements = document.getElementsByName("span-phrase");
        for (var i=0; i < phraseElements.length; i++) {
            let phraseElement = phraseElements[i].innerHTML;
            // replace the highlighted portions with the actual syntax for entities
            for (var j=0; j < HIGHLIGHT_SPAN_TAGS.length; j++) {
                let span_start_tag = HIGHLIGHT_SPAN_TAGS[j];
                while (phraseElement.indexOf(span_start_tag) > -1) {
                    let tag_index = phraseElement.indexOf(span_start_tag);
                    phraseElement = phraseElement.replace(span_start_tag, "[");
                    if (phraseElement.indexOf("</span>", tag_index) > -1) {
                        let replace_phrase = "]";
                        replace_phrase += "(" + this.state.entities[j] + ")";
                        phraseElement = phraseElement.replace("</span>", replace_phrase);
                    }
                }
            }
            
            newPhrases.push(phraseElement);
        }
        this.setState({ phrases: newPhrases });
    }

    renderEntity = (index) => {
        return (
            <div className="entity" style={{ background: ORDERED_COLORS[index] }}>
                <label className="label">
                    Entity Name:
                    <input 
                        className="label-input"
                        type="text"
                        name="entity-name"
                        placeholder="city"
                        value={this.state.entities[index]}
                        onChange={e => {this.handleEntityChange(e, index)}}
                    />
                </label>
                <div className="highlight-entities-button" onClick={() => this.turnOnHighlighting(ORDERED_COLORS[index])}>Highlight Entities</div>
            </div>
        )
    }   

    renderEntitiesCard() {
        // cap the number of entities for one intent to be 6 by removing the 
        // add more entities button when there are 6 or more entities
        return (
            <div className="intent-card grey-color" style={{width: 207}}>
                { this.state.isHighlighting &&
                    <div className="entity-buttons">
                        <div className="highlight-entities-button" onClick={() => this.doneHighlighting()}>Done Highlighting</div>
                    </div> }
                <Container className="entities-entry" style={{padding: 8}}>
                    {this.state.entities.map((val, index) => (this.renderEntity(index)))}
                </Container>
                { this.state.entities.length < 6 &&
                    <div className="add-more-button" onClick={this.handleAddMoreEntities}>⊕</div> }
            </div>
        )
        
    }

    renderEntitiesButton() {
        return (
            <div className="entities-button">
                <Button className="entities-button-style" onClick={this.toggleShowEntities}><span>Entities</span></Button>
            </div>
        )
    }

    renderIntentPhrase(idx) {
        return (
            <div>
                { this.state.isHighlighting ?
                    <div>
                        -&nbsp;
                        <span name="span-phrase"
                            className={this.state.highlightColorClass} 
                            onMouseUp={this.mouseUp}
                            style={{ fontWeight: "normal", cursor: "text" }}
                        >
                                {this.state.phrases[idx]}
                        </span>
                    </div>
                :
                    <input
                        style={{ marginTop: 8 }} 
                        type="text"
                        name={this.state.intent}
                        placeholder="make a new recipe"
                        value={this.state.phrases[idx]}
                        onChange={e => {this.handlePhraseChange(e, idx)}} 
                    />
                }
            </div>
            
        )
    }

    renderIntentCard() {
        return (
            <div className="intent-card">
                <form className="intent-form">
                    <label className="label">
                        Intent Name:
                        <input 
                            className="label-input"
                            type="text"
                            name="intent"
                            placeholder="create recipe"
                            value={this.state.intent}
                            onChange={e => this.handleIntentChange(e)}
                        />
                    </label>
                    <label className="label">
                        Intent Phrases:
                        {this.state.phrases.map((_, idx) => (this.renderIntentPhrase(idx)))}
                    </label>
                </form>
                <div className="add-more-button" onClick={this.handleAddMorePhrases}>⊕</div>
            </div>            
        )
    }

    render() {
        if (this.state.showEntities) {
            return (
                <Styles>
                    <Container className="card expanded-card">
                        {this.renderIntentCard()}
                        {this.renderEntitiesCard()}
                        {this.renderEntitiesButton()}
                    </Container>
                </Styles>
            );
        }
        return (
            <Styles>
                <Container className="card">
                    {this.renderIntentCard()}
                    {this.renderEntitiesButton()}
                </Container>
            </Styles>
        );
    }
}

export default IntentCard;