import React, { Component } from 'react';
import './RoomList.css';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import { withStyles } from "@material-ui/core/styles";
import Search from './Search';

const api = "http://data.cs.purdue.edu:20000/api/buildings/";

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
    if (this.state.redirect === true || this.state.error === true) {
      return <Search/>
    }

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

    console.log(this.state);

    return (
      <div className="RoomList">  
        <header>
          <div>
            <Button 
              color="secondary" 
              size="small" 
              variant="outlined" 
              onClick={this.submit}>
              <Icon>
                undo
              </Icon>
            </Button>
            <p>
              {this.props.building}
            </p>
          </div>
        </header>
        <ul>
          {this.state.roomArray}
        </ul>
      </div>
    );
  }
}

export default RoomList;