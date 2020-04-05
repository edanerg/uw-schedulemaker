import React, { useState, useEffect } from 'react';
import { Typography, TextField, Button, List, ListItem, Grid } from '@material-ui/core';
import Select from 'react-select'
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';
import serverURL from '../config';
import { subjects } from './coursesSearch';

const useStyles = makeStyles(theme => ({
  textbox: {
    marginBottom: theme.spacing(2),
  },
  button: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  filter: {
    width: '50%',
    marginRight: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
  filterContainer: {
    display: 'flex',
  }
}));

const defaultCourse = 'CS';

function MainPage({ user }: props) {
  const classes = useStyles();
  const [serverResponse, setServerResponse] = useState('');
  const [pastedSchedule, setPastedSchedule] = useState('');
  const [userClasses, setUserClasses] = useState([]);
  const [subjectFilter, setSubjectFilter] = useState(defaultCourse);
  const [catalog, setCatalog] = useState('');
  const [addableClasses, setAddableClasses] = useState([]);

  const uploadSchedule = () => {
    axios.post(`${serverURL}/schedule`, {
      schedule: pastedSchedule,
      classToAdd: '',
      classToRemove: '',
      username: user ? user.username : '',
    })
    .then(res => setServerResponse(res.data.result));
  };

  const addClassToUserSchedule = classToAdd => {
    axios.post(`${serverURL}/schedule`, {
      classToAdd: classToAdd,
      classToRemove: '',
      schedule: '',
      username: user ? user.username : '',
    })
    .then(res => setServerResponse(res.data.result));
  };

   const removeClassFromUserSchedule = classToRemove => {
    axios.post(`${serverURL}/schedule`, {
      classToRemove: classToRemove,
      classToAdd: '',
      schedule: '',
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
  }, [user, serverResponse, addableClasses])


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
              <Grid container>
                <Grid item xs={6}>
                  <Typography component="div" variant="h6" color="textPrimary" gutterBottom>
                    {`${c.subject} ${c.catalog_number} - ${c.class_type} ${c.section_number}`}
                  </Typography>
                  <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                    {`${c.weekdays} ${c.start_time} ${c.end_time}`}
                  </Typography>
                  <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                    {`${c.building} ${c.room}, Campus: ${c.campus}`}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Button color="primary" onClick={() => removeClassFromUserSchedule(c.id)}> Remove from schedule </Button>
                </Grid>
              </Grid>
            </ListItem>
          )
        })}
      </List>
      <Typography variant="h5" gutterBottom>
        List of Classes that fit your schedule:
      </Typography>
      <div className={classes.filterContainer}>
        <Select
          className={classes.filter}
          options={subjects}
          onChange={option => setSubjectFilter(option != null ? option.value : null)}
          isSearchable={true}
          isClearable={true}
          placeholder={subjectFilter}
        />
        <TextField
          className={classes.filter}
          type="text"
          name="catalog"
          placeholder="Course code"
          onChange={text => setCatalog(text.target.value)}
        />
      </div>
      <List>
        {addableClasses.filter(c => {
          if(c.subject === subjectFilter && c.catalog_number.includes(catalog)) return true;
          return false;
        }).map(c => {
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
                  {`${c.building} ${c.room}, Campus: ${c.campus}`}
                </Typography>
                <Button color="primary" onClick={() => addClassToUserSchedule(c.id)}> Add to schedule </Button>
              </Grid>
            </ListItem>
          )
        })}
      </List>
    </>
  )
}

export default MainPage;