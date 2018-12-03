import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import { withStyles } from "@material-ui/core/styles";
import classNames from 'classnames';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';
import RoomList from './RoomList';

const api = "localhost:5000/api/buildings/"

const styles = {
  button:{
    height: 56,
  },
  input:{
    color: 'white',
  },
  textField: {
    width: 500,
  },
  cssLabel: {
    color : 'white'
  },
  cssOutlinedInput: {
    '&$cssFocused $notchedOutline': {
      borderColor: `blue !important`,
      color: 'white',
    }
  },

  cssFocused: {
      borderColor: `blue !important`,
      color: 'white',
  },

  notchedOutline: {
    borderWidth: '1px',
    borderColor: 'white !important'
  },

};

class Search extends Component {

  constructor(){
    super()

    //Hard-coded sample room list
    //Object:
    //name: string (Room name)
    //free: boolean (If its free or used)
    //change: string (When the room changes to a different state)
    let sampleRooms = [
      {name: "Room 1", free: 1, change: "1:30"},
      {name: "Room 2", free: 1, change: "2:30"},
      {name: "Room 3", free: 0, change: "5:30"},
      {name: "Room 4", free: 0, change: "8:30"},
      {name: "Room 5", free: 0, change: "12:30"},
      {name: "Room 6", free: 1, change: "4:30"},
      {name: "Room 7", free: 1, change: "3:30"},
    ]

    this.state = {
      sampleRooms,
      query: '',
      redirect: false
    }  
  }
  // state = {
  //   query: '',
  //   redirect: false
  // }

  submit = () => {
    this.setState({
      redirect: true
    });
    console.log("CLICK");
  }
  
  render() {
    if (this.state.redirect === true) {
      console.log(this.state);
      // return <Redirect to={{
      //   pathname:'/RoomList',
      //   state: { from: this.state.sampleRooms }
      //   }}/>
      return <RoomList rooms={this.state.sampleRooms}/>
    }
    const { classes } = this.props;

    return (
      <div>
          <p>
            Room Finder
          </p>
          <div>
            <TextField 
              classes={{root: classes.textField}}
              variant="outlined" 
              label="Search Buildings..."
              autoFocus
              value={this.state.query}
              onChange={(e, newValue) => this.setState({ query: newValue})}
              InputLabelProps={{
                classes:{
                  root: classes.cssLabel,
                  focused: classes.cssFocused,
                },
              }}
              InputProps={{
                classes:{
                  root: classes.cssOutlinedInput,
                  input: classes.cssLabel,
                  notchedOutline: classes.notchedOutline,
                  focused: classes.cssFocused,
                }
              }}
            />
            <Button classes={{root: classes.button}} 
              color="secondary" 
              size="small" 
              variant="outlined" 
              onClick={this.submit}>
              <Icon>
                search
              </Icon>
            </Button>
          </div>
      </div>
    );
  }
}

export default withStyles(styles)(Search);
