import React, { Component } from 'react';
import logo from './logo.svg';
import RoomList from './RoomList';
import './App.css';

class App extends Component {

  constructor (){
    super()

    let testRooms = [
      {name: "Room 1", free: 1, change: "1:30"},
      {name: "Room 2", free: 1, change: "2:30"},
      {name: "Room 3", free: 0, change: "5:30"},
      {name: "Room 4", free: 0, change: "8:30"},
      {name: "Room 5", free: 0, change: "12:30"},
      {name: "Room 6", free: 1, change: "4:30"},
      {name: "Room 7", free: 1, change: "3:30"},
    ]

    this.state = {
      testRooms: testRooms
    }    
  }



  render() {
    return (
      <div className="App">
        <RoomList rooms={this.state.testRooms} propTest="pleaseworkman" />
      </div>
    );
  }
}

export default App;
