import React, { useState } from 'react';
import { Accordion, Alert, Card } from 'react-bootstrap';
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

const action_commands = [{
    "title": "Create a Variable",
    "examples": [
        "create a variable called foo",
        "make a variable"
    ]
},
{
    "title": "Set a Variable",
    "examples": [
        "set a variable",
        "set the variable foo to 5"
    ]
},
{
    "title": "Add to a (Number) Variable",
    "examples": [
        "add 5 to variable foo",
        "add to foo"
    ]
},
{
    "title": "Make Me Say Something",
    "examples": [
        "say 'Hello world!'",
        "say the value of the variable foo"
    ]
},
{
    "title": "Make a Conditional",
    "examples": [
        "if foo is greater than 5, say hooray",
        "if bar is less than 10, add 10 to variable bar"
    ]
},
{
    "title": "Make a While Loop",
    "examples": [
        "while foo is less than 2, add 2 to variable foo",
        "make a while loop"
    ]
},
{
    "title": "Make a Until Loop",
    "examples": [
        "add 2 to variable foo until foo is equal to 20",
        "make an until loop"
    ]
},
{
    "title": "Give a Condition (Only When Asked)",
    "examples": [
        "if foo is equal to 5",
        "until foo is greater than 2",
        "while foo is not 0"
    ]
},
{
    "title": "Get User Input",
    "examples": [
        "get user input",
        "get user input and call it foo"
    ]
},
{
    "title": "Cancel the Current Action",
    "examples": [
        "cancel"
    ]
}
]

const example_commands = {
"home": [{
        "title": "Create a Procedure or Program",
        "examples": [
            "create a procedure",
            "make a procedure called test"
        ]
    },
    {
        "title": "Run a Procedure or Program",
        "examples": [
            "run test"
        ]
    },
    {
        "title": "Edit a Procedure or Program",
        "examples": [
            "edit test",
            "open test"
        ]
    },
    {
        "title": "Rename a Procedure or Program",
        "examples": [
            "rename hello",
            "rename test to hello"
        ]
    },
    {
        "title": "Delete a Procedure or Program",
        "examples": [
            "delete hello"
        ]
    },
    {
        "title": "Connect an Intent to a Procedure or Program",
        "examples": [
            "connect the intent greet to the procedure greet me back"
        ]
    },
],
"creating": [{
    "title": "Finish Creating",
    "examples": [
        "done"
    ]
}].concat(action_commands),
"editing_action": action_commands,
"editing": [
    {
        "title": "Finish Editing Procedure or Leave Loop",
        "examples": [
            "done"
        ]
    },
    {
        "title": "Navigate Through Procedure",
        "examples": [
            "next step",
            "previous step",
            "go to step 5",
            "go to the first step",
            "go to the last step"
        ]
    },
    {
        "title": "Add a New Action",
        "examples": [
            "add step",
            "make a new step",
            "create a new step"
        ]
    },
    {
        "title": "Delete Current Action",
        "examples": [
            "remove step",
            "delete step"
        ]
    },
    {
        "title": "Change or Replace Current Action",
        "examples": [
            "change step",
            "replace step"
        ]
    },
    {
        "title": "Step Into Loop",
        "examples": [
            "step into"
        ]
    }
].concat(action_commands),
"executing": [{
    "title": "Stop Currently Running Procedure",
    "examples": [
        "stop",
        "cancel"
    ]
}]
}

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

    .sidebar-container {
        grid-column-start: 1;
        grid-column-end: 3;
        grid-row-start: 1;
        grid-row-end: 6;
        overflow: auto;
    }

    .sidebar {
        display: flex;
        text-align: center;
        flex-direction: column;
    }

    .voice-text-container {
        grid-column-start: 3;
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

const ProgramPage = (props) => {
    const [state, setState] = useState('home');

    const callbackFunction = (childState) => {
        setState(childState);
    }

    const renderSidebar = () => {

        const renderInfo = () => {
            return (
                <Alert className="info-alert" variant='info'>
                    <div><b>You are in sandbox mode.</b></div>
                    <div><em>Stuck? If stuck for 5 minutes, say "I need help".</em></div>
                </Alert>
            )
        }

        const renderExampleProgramsAccordion = () => {
            return (
                <Accordion style={{ marginBottom: '10px' }}>
                    <Card style={{ cursor: 'pointer' }}>
                        <Accordion.Toggle as={Card.Header} eventKey="0">
                            Example Programs
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="0">
                        <Card.Body style={{ textAlign: 'left'}}>
                            {renderExamplePrograms()}
                        </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
            )
        }

        const renderExamplePrograms = () => {
            return (
                <div>
                    <div><b>Hello World!</b></div>
                    <ol>
                        <li>Say <em>"Create a procedure called hello"</em></li>
                        <li>Say <em>"Say hello world"</em></li>
                        <li>Say <em>"Done"</em></li>
                        <li>Say <em>"Run hello"</em></li>
                    </ol>
                </div>
            )
        }

        const renderExampleActionsAccordion = () => {
            return (
                <Accordion>
                    <Card style={{ cursor: 'pointer' }}>
                        <Accordion.Toggle as={Card.Header} eventKey="1">
                            Things You Can Say To...
                        </Accordion.Toggle>
                        <Accordion.Collapse eventKey="1">
                            <Card.Body style={{ textAlign: 'left' }}>
                                {renderExampleActions(state)}
                            </Card.Body>
                        </Accordion.Collapse>
                    </Card>
                </Accordion>
            )
        }
    
        const renderExampleActions = (state) => {
            return (
                <div>
                    {Object.entries(example_commands[state]).map(([key, action]) => {return renderExampleAction(action)})}
                </div>
            )
        }
    
        const renderExampleAction = (action) => {
            return (
                <div className="example-action" style={{ marginBottom: '10px' }}>
                    <div className="action-title"><b>{action.title}</b></div>
                    {action.examples.map(ex => {
                        return (<div><em>{ex}</em></div>)
                    })}
                </div>
            )
        };

        return (
            <div className="sidebar-container">
                <div className="sidebar">
                    {renderInfo()}
                    {renderExampleProgramsAccordion()}
                    {renderExampleActionsAccordion()}
                </div>
            </div>
        )
    };

    return (
        <Styles>
            <div className="experiment-container">
                {renderSidebar()}
                <ChatBox sid={props.sid} isUnconstrained={false} pageId={"program"} state={state} parentCallback={callbackFunction} socketNode={props.socketNode} socketFlask={props.socketFlask}/>
            </div>
        </Styles>
    )
}

export default ProgramPage;