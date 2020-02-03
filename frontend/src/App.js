import React, { Component } from 'react';
import ClassSearch from './components/classSearch';
import Bar from './components/bar';
import Login from './components/login';
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import { amber, grey } from '@material-ui/core/colors';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import './App.css';
import serverURL from './config';
import axios from 'axios';

const theme = createMuiTheme({
  palette: {
    primary: amber,
    secondary: grey
  }
});

const defaultCourses = [
  {   id: "1",
      name: "JJ101",
      subject: "SS",
      catalog_number: "SSS",
      description: "fuck",
      time: "MWF 9:00-10:20",
      instructor: "Kujo Jotaro",
      location: "Egypt"
  },
  {   id: "2",
      name: "JJ201",
      time: "F 19:00-21:00",
      subject: "SS",
      catalog_number: "SSS",
      description: "fuck",
      instructor: "Johny Jostar",
      location: "The Wild Wacky West"
  },
  {   id: "3",
      name: "JJ301",
      time: "M 19:00-21:00",
      subject: "SS",
      catalog_number: "SSS",
      description: "fuck",
      instructor: "Jonathon Jostar",
      location: "Some Ramdom English Mansion"
  },
  {   id: "4",
      name: "JJ401",
      time: "MW 12:00-13:30",
      subject: "SS",
      catalog_number: "SSS",
      description: "fuck",
      instructor: "Higashikata Josuke",
      location: "Morioh"
  }
]

class App extends Component {

  state = {
    courses: [],
    user: null
  }

  setUser = user => {
    this.setState({
      user: user
    })
  }

  setCourses = courses => {
    this.setState({
      courses: courses
    })
  }

  componentDidMount() {
    axios.get(`${serverURL}/courses`).then(res => {
      this.setState({
        courses: res.data.courses
      })
    })
  }

  render() {
    return (
      <ThemeProvider theme={theme}>
        <Router>
        <Bar user={this.state.user} setUser={this.setUser}/>
        <div className="App">
          <div className="app-body">
              <Switch>
                <Route exact path="/">
                  <ClassSearch user={this.state.user} courses={this.state.courses} setUser={this.setUser} setCourses={this.setCourses} />
                </Route>
                <Route exact path="/login">
                  <Login user={this.state.user} setUser={this.setUser} setCourses={this.setCourses}/>
                </Route>
                <Route render={() => <Redirect to={{pathname: "/"}} />} />
              </Switch>
          </div>
        </div>
        </Router>
      </ThemeProvider>
    );
  }
}

export default App;
