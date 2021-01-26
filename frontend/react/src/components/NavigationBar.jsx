import React from 'react';
import { Nav, Navbar } from 'react-bootstrap';
import Link from 'react-router-dom/Link';
import styled from 'styled-components';

const Styles = styled.div`
    .navbar {
        background-color: #34AEA6;
    }

    a, .navbar-brand, .navbar-nav .nav-link {
        color: white;

        &:hover {
            color: white;
        }
    }
`;

export const NavigationBar = () => (
    <Styles>
        <Navbar expand="lg" variant="dark">
            <Navbar.Brand><Link to="/">Convo</Link></Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ml-auto">
                <Nav.Item><Nav.Link><Link to="/create-intents">Create Intents</Link></Nav.Link></Nav.Item>
                <Nav.Item><Nav.Link><Link to="/program">Program</Link></Nav.Link></Nav.Item>
                <Nav.Item><Nav.Link><Link to="/talk-to-convo">Talk to Convo</Link></Nav.Link></Nav.Item>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    </Styles>
)