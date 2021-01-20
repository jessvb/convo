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

const ORDERED_COLORS = [COLORS.yellow, COLORS.blue, COLORS.red, COLORS.green, COLORS.purple, COLORS.orange];

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
            phrases: [''],
            entities: [''],
            showEntities: false,
            highlightColor: '',
            highlightColorClass: 'label-input',
        };
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

    turnOnHighlighting = (color) => {
        console.log(color);
        let color_name = HEX_TO_COLOR[color];
        this.setState({ highlightColorClass: `label-input-${color_name}`, highlightColor: color });
    }

    mouseUp = () => {
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
    }

    renderEntity = (color) => {
        return (
            <div className="entity" style={{ background: color }}>
                <label className="label">
                    Entity Name:
                    <input className="label-input" type="text" name="entity-name" placeholder="city"/>
                </label>
                <div className="highlight-entities-button" onClick={() => this.turnOnHighlighting(color)}>Highlight Entities</div>
            </div>
        )
    }   

    renderEntitiesCard() {
        // cap the number of entities for one intent to be 6
        if (this.state.entities.length < 6) {
            return (
                <div className="intent-card grey-color" style={{width: 207}}>
                    <Container className="entities-entry" style={{padding: 8}}>
                        {this.state.entities.map((val, index) => (this.renderEntity(ORDERED_COLORS[index])))}
                    </Container>
                    <div className="add-more-button" onClick={this.handleAddMoreEntities}>⊕</div>
                </div>
            )
        }

        // remove the add more entities button
        return (
            <div className="intent-card grey-color" style={{width: 207}}>
                <Container className="entities-entry" style={{padding: 8}}>
                    {this.state.entities.map((val, index) => (this.renderEntity(ORDERED_COLORS[index])))}
                </Container>
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

    renderIntentCard() {
        return (
            <div className="intent-card">
                <form className="intent-form">
                    <label className="label">
                        Intent Name:
                        <input className="label-input" type="text" name="name" placeholder="create recipe"/>
                    </label>
                    <label className="label">
                        Intent Phrases:
                        {this.state.phrases.map(() => (<input className={this.state.highlightColorClass} type="text" name="phrases" id="phrases" placeholder="make a new recipe" onMouseUp={this.mouseUp}/>))}
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