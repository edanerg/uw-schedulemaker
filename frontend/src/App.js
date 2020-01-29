import React, { useEffect, useState } from 'react';
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

function App() {
  // Testing connection with backend
  /*
  const [backendMessage, setBackendMessage] = useState('');
  
   useEffect(() => {
    fetch(`${serverURL}/courses`)
      .then(response => response.json())
      .then(data => {
        const { courses } = data;
        setBackendMessage(courses);
      })
      .catch(err => {
        setBackendMessage("Error getting info");
        console.error(err);
      });
  }, []); */

  return (
    <ThemeProvider theme={theme}>
      <Bar/>
      <div className="App">
        <div className="app-body">
          <div className="search-criteria">
            <TimeSelect/>
          </div>
          <ClassList/>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
