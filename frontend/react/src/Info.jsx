import React from 'react';
import styled from 'styled-components';

const Styles = styled.div`
    .text-body {
        width: 70%;
        margin: auto;
        text-align: justify;
    }

    .center-text {
        text-align: center;
    }
`

export const Info = () => (
    <Styles>
        <div>
            <h1 style={{ marginTop: 20, textAlign: 'center' }}>Create Your Own Conversational AI Agents</h1>
            <h3 className='center-text'>Welcome!</h3>
            <div className='text-body'>
                <p>
                    <strong>Conversational AI agents</strong> like Apple Siri, Amazon Alexa, and Google Home 
                    are becoming increasingly commonplace. We are interested in making this technology more 
                    accessible to students by lowering the barrier to entry. 
                    We have created <strong>Convo</strong>, a conversational programming agent, that allows anyone to
                    envision and create their own conversational AI agents.
                    During this class, you will learn how to use <strong>Convo</strong> to create your own conversational AI agents.
                    You'll then be able to speak to the agents you created in a natural, intuitive way. 
                </p>
                <p>
                    <strong>Convo</strong> consists of three parts, seen in the header of this website:
                    <ol>
                        <li>
                            <strong>Create Intents</strong>
                        </li>
                        <li>
                            <strong>Program</strong>
                        </li>
                        <li>
                            <strong>Talk To Convo</strong>
                        </li>
                    </ol>
                </p>
                <p>
                    The <strong>Create Intents</strong> page is where you tell <strong>Convo</strong> about 
                    the <strong>intents</strong> and <strong>entities</strong> you'd like <strong>Convo</strong> to
                    recognize. You will also provide training data so that <strong>Convo</strong> can learn how to
                    understand what you say to it. For example, you might want <strong>Convo</strong> to recognize
                    when you are saying hello and goodbye. To do this, you'd add in two intents, one for hello and one
                    for goodbye. Example training data you might enter for hello would be: "hello", "hi", "hey", 
                    "hey there", "what's up?" and example training data for goodbye might be: "bye", "goodbye", 
                    "farewell", "until next time". The more training data you provide, the more <strong>Convo</strong> will 
                    be able to learn. <strong>Entities</strong> are specific pieces of data that you'd like to extract 
                    from an <strong>intent</strong>, like a name, but they are optional.
                </p>
                <p>
                    The <strong>Program</strong> page is where you can create the procedures and actions you want to 
                    happen when Convo recognizes one of the intents from the <strong>Create Intents</strong> page. Once 
                    you have finished training your intents, you can then connect that intent to a procedure. 
                    This page uses a <strong>constrained natural language</strong> model, which means that you must 
                    follow the instructions in the sidebar when creating your procedure for <strong>Convo</strong> to
                    understand you.
                </p>
                <p>
                    The <strong>Talk To Convo</strong> page is where you can test out your conversational AI agent by
                    speaking or typing to Convo in a conversational manner. When <strong>Convo</strong> recognizes 
                    an intent that was trained on in the <strong>Create Intents</strong> page, it will trigger the 
                    procedure it was connected to in the <strong>Program</strong> page. You'll notice that there is no 
                    sidebar with instructions on how to speak to <strong>Convo</strong> because this page uses
                    an <strong>unconstrained natural language</strong> model, which means that <strong>Convo</strong> is
                    able to understand a wider variety of natural conversation.
                </p>
                <p className="center-text">
                    Please watch the videos below if you would like to see how the system works.
                </p>
                <p align="center">
                    <iframe width="560" height="315" src="https://www.youtube.com/embed/K-NppKDKzDY" 
                        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </p>
                <p align="center">
                    <iframe width="560" height="315" src="https://www.youtube.com/embed/Yio48CwVaR4" 
                        frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </p>
                <p>
                    As always, we welcome feedback to improve <strong>Convo</strong>! If you have any suggestions, please 
                    fill out this <a href="https://forms.gle/zWuFjAxtvtywkagAA" target="_blank">form</a>. 
                    Thank you for trying out <strong>Convo</strong>.
                </p>
            </div>
        </div>
    </Styles>
    
)
