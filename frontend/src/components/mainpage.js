import React, { useState } from 'react';
import { Typography, TextField, Button, List, ListItem } from '@material-ui/core';
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
  }
}));

function MainPage({ user }: props) {
  const classes = useStyles();
  const [pastedSchedule, setPastedSchedule] = useState('Class Nbr\n6439\n Class Nbr\n6345\nClass Nbr\n8648');
  const [userClasses, setUserClasses] = useState([]);

  const uploadSchedule = () => {
    axios.post(`${serverURL}/schedule`, {
      schedule: pastedSchedule
    })
    .then(res => setUserClasses(res.data.classes));
  };

  return (
    <>
      <Typography variant="h5" gutterBottom>
        (Work in progress)
      </Typography>
      <br/><br/><br/>
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
        rowsMax="5"
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
            <ListItem key={c.class_number}>
              <Typography variant="body1" color="textPrimary" gutterBottom>
                  {`${c.subject} ${c.catalog_number} ${c.class_type} ${c.section_number}`}
              </Typography>
            </ListItem>
          )
        })}
      </List>
      <Typography variant="h5" gutterBottom>
        Classes you can add
      </Typography>
      {console.log(userClasses)}
    </>
  )
}

export default MainPage;