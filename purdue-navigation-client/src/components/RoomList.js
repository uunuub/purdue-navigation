import React, { Component } from 'react';
import './RoomList.css';

class RoomList extends Component {

  constructor (props){
    //Accept list of rooms from App.js
    super(props);
    let rooms = this.props.rooms;
    console.log("PRINT ROOMS AYY");
    console.log(rooms);
    let roomArray = [];

    //Converts the list of rooms to HTML Elements
    for (let i = 0; i < rooms.length; i++){
      if (rooms[i].free === 1){
        roomArray.push(React.createElement("li", {className: "Room-box-free"}, (rooms[i].name + " - Free until " + rooms[i].change)));
      }
      else{
        roomArray.push(React.createElement("li", {className: "Room-box-used"}, (rooms[i].name + " - Used until " + rooms[i].change)));
      }
    }

    this.state = {
      roomArray
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
          {this.state.roomArray}
        </ul>
      </div>
    );
  }
}

export default RoomList;