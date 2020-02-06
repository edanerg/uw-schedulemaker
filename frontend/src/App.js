import React, { useState, useEffect } from 'react';
import ClassSearch from './components/classSearch';
import CoursesSearch from './components/coursesSearch';
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

function App(){

  const [coursesTaken, setCoursesTaken] = useState([]);
  const [user, setUser] = useState(null);
  const [classes, setClasses] = useState([]);
  const [courses, setCourses] = useState([]);


  useEffect(() => {
    axios.get(`${serverURL}/class`).then(res => {
      setClasses(res.data.classes);
    })
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <Router>
      <Bar user={user} setUser={setUser} setCoursesTaken={setCoursesTaken}/>
      <div className="App">
        <div className="app-body">
            <Switch>
              <Route exact path="/">
                <ClassSearch user={user} classes={classes} setUser={setUser} setClasses={setClasses} />
              </Route>
              <Route exact path="/login">
                <Login user={user} setUser={setUser} setCoursesTaken={setCoursesTaken}/>
              </Route>
              <Route exact path="/courseHistory">
              </Route>
              <Route exact path="/courses">
                <CoursesSearch courses={courses} setCourses={setCourses} />
              </Route>
              <Route render={() => <Redirect to={{pathname: "/"}} />} />
            </Switch>
        </div>
      </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
