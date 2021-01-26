import React from 'react';
import { Container } from 'react-bootstrap';
import styled from 'styled-components';
import speechImage from '../assets/speechImage.jpg';

const Styles = styled.div`
    .jumbo {
        background: url(${speechImage}) no-repeat fixed bottom;
        background-size: cover;
        color: #efefef;
        height: 200px;
        position: relative;
        z-index: -50;
    }

    .overlay {
        background-color: #000
        opacity: 0.6;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        z-index: -25;
    }
`;

export const Jumbotron = () => (
    <Styles>
        <div className="overlay"></div>
        <Container>
            <h1>Convo</h1>
            <p>
                Program by speaking
            </p>
        </Container>
    </Styles>
)