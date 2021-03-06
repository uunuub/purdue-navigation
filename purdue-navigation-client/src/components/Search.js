import React, { Component } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Icon from '@material-ui/core/Icon';
import { withStyles } from "@material-ui/core/styles";
import classNames from 'classnames';
import PropTypes from 'prop-types';
import RoomList from './RoomList';
import './Search.css';

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

let stat = null;

class Search extends Component {
  constructor(props){
    super(props);

    this.state = {
      isLoaded: false,
      query: '',
      redirect: false,
      //status: this.props.status,
    }

    if(this.props.status == "error"){
      stat="That Building Does Not Exist";
    }else{
      stat = null;
    }
  }
  
  handleInputChange = (e) =>{
    this.setState({
      query: e.target.value,
    });
  }

  submit = () => {
    this.setState({
      redirect: true
    });
  }

  render() {
    if (this.state.redirect === true) {
      console.log(this.state);
      return <RoomList building={this.state.query}/>
    }

    const { classes } = this.props;

    return (
      <div>
          <p className="txt">
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
            <Button className="btn"
              classes={{root: classes.button}} 
              color="secondary" 
              size="small" 
              variant="outlined" 
              onClick={this.submit}>
              <Icon>
                search
              </Icon>
            </Button>
          </div>
          <div className="error">
            {stat}
          </div>
      </div>
    );
  }
}

export default withStyles(styles)(Search);
