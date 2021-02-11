import React, { Component } from 'react';
import Router from 'react-router-dom/BrowserRouter';
import Route from 'react-router-dom/Route';
import Switch from 'react-router-dom/Switch';
import { Info } from './Info';
import CreateIntentPage from './CreateIntentPage';
import ProgramPage from './ProgramPage';
import TalkToConvoPage from './TalkToConvoPage';
import { NoMatch } from './NoMatch';
import { Layout } from './components/Layout';
import { NavigationBar } from './components/NavigationBar';
import socketIOClient from 'socket.io-client';

const NODE_ENDPOINT = "http://localhost:8080";
const FLASK_ENDPOINT = "http://localhost:5000"; 

// Parse user agent string by looking for recognized substring.
const findFirstString = (str, choices) => {
    for (let j = 0; j < choices.length; j++) {
        if (str.indexOf(choices[j]) >= 0) {
            return choices[j];
        }
    }
    return '0';
};

const getUniqueId = () => {
  if (!('sid' in localStorage)) {
    let browser = findFirstString(navigator.userAgent, [
        'Seamonkey', 'Firefox', 'Chromium', 'Chrome', 'Safari', 'OPR', 'Opera',
        'Edge', 'MSIE', 'Blink', 'Webkit', 'Gecko', 'Trident', 'Mozilla'
    ]);
    let os = findFirstString(navigator.userAgent, [
        'Android', 'iOS', 'Symbian', 'Blackberry', 'Windows Phone',
        'Windows', 'OS X', 'Linux', 'iOS', 'CrOS'
    ]).replace(/ /g, '_');
    let unique = ('' + Math.random()).substr(2);
    localStorage.setItem('sid', `${os}_${browser}_${unique}_react`);
  }

  return localStorage.getItem('sid');
};

class App extends Component {
  constructor(props) {
      super(props);

      this.state = {
          sid: getUniqueId(),
          socketNode: socketIOClient(NODE_ENDPOINT),
          socketFlask: socketIOClient(FLASK_ENDPOINT)
      }
  }
  componentDidMount() {
    localStorage.setItem('currPart', 'sandbox');
    localStorage.setItem('currStage', 'sandbox');
    this.configureSocket();
  }

  configureSocket = () => {    
    this.state.socketNode.on('reactconnection', () => {
      console.log('Connected to the Node app');
    });

    this.state.socketFlask.on('connect', (data) => {
        console.log('Connected to the Flask backend');
        this.state.socketFlask.emit('join', {
            "sid": this.state.sid,
            "stage": localStorage.getItem('currStage'),
            "part": localStorage.getItem('currPart')
        });
    });

    this.state.socketFlask.on('joined', (data) => {
        console.log("Socket connected to API server.");
        console.log(`SID returned from API server: ${data}`);
    });

    this.state.socketFlask.on('error', function (err) {
        console.log(err);
    });
  }
  

  render() {
    return (
      <React.Fragment>
        <Router>
          <NavigationBar />
          <Layout>
            <Switch>
              <Route exact path="/" component={Info} />
              <Route path="/create-intents" render={() => <CreateIntentPage sid={this.state.sid} socketFlask={this.state.socketFlask} />} />
              <Route path="/program" render={() => <ProgramPage sid={this.state.sid} socketNode={this.state.socketNode} socketFlask={this.state.socketFlask} />} />
              <Route path="/talk-to-convo" render={() => <TalkToConvoPage sid={this.state.sid} socketNode={this.state.socketNode} socketFlask={this.state.socketFlask} />} />
              <Route component={NoMatch} />
            </Switch>
          </Layout>
        </Router>
      </React.Fragment>
      
    );
  }
  
}

export default App;
