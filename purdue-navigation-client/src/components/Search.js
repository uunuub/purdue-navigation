import React, { Component } from 'react';
import SearchBar from 'material-ui-search-bar'

class Search extends Component {

  state = {
    query: '',
  }

  handleInputChange = () => {
    this.setState({
      query: this.search.value
    })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <p>
            Is It Empty???
          </p>
          <form>
            <input
              placeholder="Search buildings..."
              ref = {input => this.search = input}
              onChange = {this.handleInputChange}/>
          </form>
          <button>Search</button>
        </header>
      </div>
    );
  }
}

export default Search;
