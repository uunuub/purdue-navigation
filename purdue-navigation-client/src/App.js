import React, { Component } from 'react';
import logo from './logo.svg';
import Search from './components/Search';
import './App.css';
import RoomList from './components/RoomList';
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from "react-router-dom";


class App extends Component {
  render() {
    return (
    <Router>
      <div >
        <header className="App-header">
          <Search status=""/>
        </header>
        <Route path="/RoomList" component={RoomList} />
      </div>
      </Router>
    );
  }
}

export default App;
