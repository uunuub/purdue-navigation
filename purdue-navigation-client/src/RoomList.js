import React, { Component } from 'react';
import './RoomList.css';

class RoomList extends Component {

  constructor (props){
    super(props)
    // this.constructor.bind(this)

    let testRooms = this.props.rooms
    let roomArray = []

    for (let i = 0; i < testRooms.length; i++){
      if (testRooms[i].free === 1){
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
            {this.props.propTest}
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