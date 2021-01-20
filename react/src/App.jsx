import React, { Component } from 'react';
import Router from 'react-router-dom/BrowserRouter';
import Route from 'react-router-dom/Route';
import Switch from 'react-router-dom/Switch';
import { Info } from './Info';
import CreateIntentPage from './CreateIntentPage';
import { ProgramPage } from './ProgramPage';
import { TalkToConvoPage } from './TalkToConvoPage';
import { NoMatch } from './NoMatch';
import { Layout } from './components/Layout';
import { NavigationBar } from './components/NavigationBar';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <Router>
          <NavigationBar />
          <Layout>
            <Switch>
              <Route exact path="/" component={Info} />
              <Route path="/create-intents" component={CreateIntentPage} />
              <Route path="/program" component={ProgramPage} />
              <Route path="/talk-to-convo" component={TalkToConvoPage} />
              <Route component={NoMatch} />
            </Switch>
          </Layout>
        </Router>
      </React.Fragment>
    );
  }
}

export default App;
