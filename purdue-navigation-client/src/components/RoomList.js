import React, { Component } from 'react';
import './RoomList.css';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import { withStyles } from "@material-ui/core/styles";
import Search from './Search';

const api = window.location.origin + "/api/buildings/";

class RoomList extends Component {

  constructor (props){
    //Accept list of rooms from App.js
    super(props);
    this.state = {
      building: this.props.building,
      rooms: [],
      redirect: false,
      error: false,
    }
  }

  componentDidMount(){
    const fullRequest = api + this.props.building;

    fetch(fullRequest)
      .then(res => res.json())
      .then(
        (result) => {
          // Save actual name of building
          let actualName = result["Building"]
          result = result["Rooms"]
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
            buildingName: actualName
          })
        },
        (error) => {
          this.setState({
            error: true,
          });
        }
      )
  }

  submit = () => {
    this.setState({
      redirect: true
    });
  }

  render() {
    if (this.state.redirect === true) {
      return <Search status=""/>
    }

    if(this.state.error === true){
      return <Search status="error"/>
    }

    let roomArray = [];
    let buildingName = this.state.buildingName;

    //Converts the list of rooms to HTML Elements
    for (let i = 0; i < this.state.rooms.length; i++){
      if (this.state.rooms[i].free === true){
        roomArray.push(React.createElement("li", {className: "Room-box-free"}, (this.state.rooms[i].name + " - Free until " + this.state.rooms[i].change)));
      }
      else{
        roomArray.push(React.createElement("li", {className: "Room-box-used"}, (this.state.rooms[i].name + " - Used until " + this.state.rooms[i].change)));
      }
    }
    this.state ={
      roomArray: roomArray,
      buildingName: buildingName
    };

    return (
      <div>
        <div className="btn">
          <Button 
            color="secondary" 
            size="small" 
            variant="outlined" 
            onClick={this.submit}>
            <Icon>
              undo
            </Icon>
          </Button>
        </div>
        <div className="RoomList">  
          <header>
            <div>
              <p>
                {this.state.buildingName}
              </p>
            </div>
          </header>
          <ul>
            {this.state.roomArray}
          </ul>
        </div>
      </div>
    );
  }
}

export default RoomList;