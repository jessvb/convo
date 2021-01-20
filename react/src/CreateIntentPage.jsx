import React, { Component } from 'react';
import { Container } from 'react-bootstrap';
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

class CreateIntentPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            intents: [''],
        };
    }

    handleAddMoreIntents = () => {
        let oneMoreIntent = this.state.intents.concat([''])
        this.setState({ intents: oneMoreIntent })
    }

    renderIntentCardAddMoreButton() {
        return (
            <Container className="add-more" onClick={this.handleAddMoreIntents}>
                <div className="add-more-intents-button">
                    <div className="add-more-button">⊕</div>
                </div>
                <div className="sidebar"></div>
            </Container>
        );
    }

    render() {
        return (
            <Styles>
                <div className="intent-page">
                {this.state.intents.map(() => (<IntentCard/>))}
                    {this.renderIntentCardAddMoreButton()}
                </div>
            </Styles>
        )
    }
}

export default CreateIntentPage;