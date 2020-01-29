import React, { Component } from 'react';
import TimeSelect from './components/timeSelect';
import ClassList from './components/classList';
import Bar from './components/bar';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { amber, grey } from '@material-ui/core/colors';
import './App.css';

let serverURL = process.env.REACT_APP_SERVER_URL;

const theme = createMuiTheme({
  palette: {
    primary: amber,
    secondary: grey
  }
});

class App extends Component {

  state = {
    courses: [],
  }

  async componentDidMount() {
    const response = await fetch(`${serverURL}/courses`);
    const { courses } = await response.json();
    console.log('Courses', courses);
    this.setState({ courses });
  }

  render() {
    return (
      <ThemeProvider theme={theme}>
        <Bar/>
        <div className="App">
          <div className="app-body">
            <div className="search-criteria">
              <TimeSelect/>
            </div>
            <ClassList courses={this.state.courses}/>
          </div>
        </div>
      </ThemeProvider>
    );
  }
}

export default App;
