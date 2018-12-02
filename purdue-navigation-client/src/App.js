import React, { Component } from 'react';
import logo from './logo.svg';
import RoomList from './RoomList';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <RoomList />
      </div>
    );
  }
}

export default App;
