import React, { Component } from 'react';
import './RoomList.css';

const api = "http://data.cs.purdue.edu:20000/api/buildings/"


class RoomList extends Component {

  constructor (props){
    //Accept list of rooms from App.js
    super(props);
    this.state = {
      building: this.props.building,
      rooms: [],
    }
  }

  componentDidMount(){
    const fullRequest = api + this.props.building;

    fetch(fullRequest)
      .then(res => res.json())
      .then(
        (result) => {
          let tempArr = []
          Object.keys(result).forEach(function(key) {
            let roomObj = {
              name:key,
              free:result[key][0],
              change:result[key][1]
            }
            tempArr.push(roomObj);
          });

          this.setState({
            rooms: tempArr,
          })
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
    } 

  render() {
    console.log("PRINT ROOMS AYY");
    console.log(this.state);
    let roomArray = [];

    //Converts the list of rooms to HTML Elements
    for (let i = 0; i < this.state.rooms.length; i++){
      if (this.state.rooms[i].free === true){
        roomArray.push(React.createElement("li", {className: "Room-box-free"}, (this.state.rooms[i].name + " - Free until " + this.state.rooms[i].change)));
      }
      else{
        roomArray.push(React.createElement("li", {className: "Room-box-used"}, (this.state.rooms[i].name + " - Used until " + this.state.rooms[i].change)));
      }
    }

    this.state = {
      roomArray
    }   

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