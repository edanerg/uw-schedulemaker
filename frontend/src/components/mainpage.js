import React, { useState, useEffect } from 'react';
import { Typography, TextField, Button, List, ListItem, Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';
import serverURL from '../config';

const useStyles = makeStyles(theme => ({
  textbox: {
    marginBottom: theme.spacing(2),
  },
  button: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
}));

function MainPage({ user }: props) {
  const classes = useStyles();
  const [serverResponse, setServerResponse] = useState('');
  const [pastedSchedule, setPastedSchedule] = useState('');
  const [userClasses, setUserClasses] = useState([]);
  const [addableClasses, setAddableClasses] = useState([]);

  const uploadSchedule = () => {
    axios.post(`${serverURL}/schedule`, {
      schedule: pastedSchedule,
      username: user ? user.username : '',
    })
    .then(res => setServerResponse(res.data.result));
  };

  useEffect(() => {
    axios.get(`${serverURL}/schedule`, {params: 
      {username: user ? user.username : ''}
    }).then(res => {
      if (user) setAddableClasses(res.data.addable_classes)
      setUserClasses(res.data.schedule)
    });
  }, [user, serverResponse])

  return (
    <>
      <Typography variant="h5" gutterBottom>
          Schedule
      </Typography>
      <Typography variant="body1" gutterBottom>
          To upload your schedule, go to Quest->class schedule. Select all, copy and paste it in the text box below
      </Typography>
      <TextField
        className={classes.textbox}
        fullWidth
        multiline
        rowsMax="9"
        value={pastedSchedule}
        onChange={e => setPastedSchedule(e.target.value)}
        margin="normal"
        variant="outlined"
      />
      <Button
        className={classes.button}
        variant="outlined"
        color="primary"
        onClick={uploadSchedule}
      >
        Upload
      </Button>
      <Typography variant="h5" gutterBottom>
        Your Classes
      </Typography>
      <List>
        {userClasses.map(c => {
          return (
            <ListItem component="div" key={c.id}>
              <Grid>
                <Typography component="div" variant="h6" color="textPrimary" gutterBottom>
                  {`${c.subject} ${c.catalog_number} - ${c.class_type} ${c.section_number}`}
                </Typography>
                <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                  {`${c.weekdays} ${c.start_time} ${c.end_time}`}
                </Typography>
                <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                  {`${c.building} ${c.room}`}
                </Typography>
              </Grid>
            </ListItem>
          )
        })}
      </List>
      <Typography variant="h5" gutterBottom>
        List of Classes that fit your schedule:
      </Typography>
      <List>
        {addableClasses.map(c => {
          return (
            <ListItem component="div" key={c.id}>
              <Grid>
                <Typography component="div" variant="h6" color="textPrimary" gutterBottom>
                  {`${c.subject} ${c.catalog_number} - ${c.class_type} ${c.section_number}`}
                </Typography>
                <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                  {`${c.weekdays} ${c.start_time} ${c.end_time}`}
                </Typography>
                <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                  {`${c.building} ${c.room}`}
                </Typography>
              </Grid>
            </ListItem>
          )
        })}
      </List>
    </>
  )
}

export default MainPage;