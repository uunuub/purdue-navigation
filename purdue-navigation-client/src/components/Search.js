import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import { withStyles } from "@material-ui/core/styles";
import classNames from 'classnames';
import PropTypes from 'prop-types';
import { Redirect } from 'react-router-dom';
import RoomList from './RoomList';

const api = "http://data.cs.purdue.edu:20000/api/buildings/"

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

    this.state = {
      isLoaded: false,
      query: '',
      rooms: [],
      redirect: false,
    }  
  }
  
  handleInputChange = (e) =>{
    this.setState({
      query: e.target.value,
    });
  }

  submit = () => {
    const fullRequest = api + this.state.query
    fetch(fullRequest)
      .then(res => res.json())
      .then(
        (result) => {
          let roomArr = [];

          Object.keys(result).forEach(function(key) {
            let roomObj = {
              name:key,
              free:result[key][0],
              change:result[key][1]
            }
            //console.log(result[key]);
            //console.log(roomObj);
            roomArr.push(roomObj);
          });

          this.setState({
            rooms: roomArr,
          })
          //console.log(this.state);
          // this.setState({
          //   sampleRooms: roomArr,
          // })
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )

    this.setState({
      redirect: true
    });
  }
  
  render() {
    console.log(this.state);
    
    if (this.state.redirect === true) {
      return <RoomList rooms={this.state.rooms}/>
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
              onChange={this.handleInputChange}
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
