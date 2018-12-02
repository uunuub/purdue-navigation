import React, { Component } from 'react';
import './RoomList.css';

class RoomList extends Component {

  constructor (){
    super()

    let testRooms = [
      {name: "Room 1", free: 0, change: "1:30"},
      {name: "Room 2", free: 0, change: "2:30"},
      {name: "Room 3", free: 1, change: "5:30"},
      {name: "Room 4", free: 1, change: "8:30"},
      {name: "Room 5", free: 1, change: "12:30"},
      {name: "Room 6", free: 0, change: "4:30"},
      {name: "Room 7", free: 0, change: "3:30"},
    ]

    let roomArray = []

    for (let i = 0; i < testRooms.length; i++){
      if (testRooms[i].free === 0){
        roomArray.push(React.createElement("li", {className: "Room-box-free"}, (testRooms[i].name + " - Free until " + testRooms[i].change)))
      }
      else{
        roomArray.push(React.createElement("li", {className: "Room-box-used"}, (testRooms[i].name + " - Used until " + testRooms[i].change)))
      }
    }

    this.state = {
      roomList: roomArray
    }    
  }

  render() {
    return (
      <div className="RoomList">  
      
        <header>
          <p>
            Building
          </p>
        </header>

        <ul>
          {this.state.roomList}
        </ul>

      </div>
    );
  }
}

export default RoomList;