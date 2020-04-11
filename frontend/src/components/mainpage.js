import React, { useState, useEffect } from 'react';
import { Typography, TextField, Button, List, ListItem, Grid } from '@material-ui/core';
import Select from 'react-select'
import { makeStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
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
  const [dialogTitle, setDialogTitle] = useState('');
  const [dialogText, setDialogText] = useState('');
  const [allowedRel1, setAllowedRel1] = useState([]);
  const [allowedRel2, setAllowedRel2] = useState([]);
  const [rel1Value, setRel1Value] = useState(0);
  const [rel2Value, setRel2Value] = useState(0);
  const [showRel1, setShowRel1] = useState({display: 'none'});
  const [showRel2, setShowRel2] = useState({display: 'none'});
  const [addOpen, setAddOpen] = useState(false);
  const [removeOpen, setRemoveOpen] = useState(false);
  const [classSelected, setClassSelected] = useState(null);

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

  const getRelated1Note = c => {
    if (c.section_number.charAt(0) === '0') {
      switch(c.rel_1) {
        case 0: return ""
        case 1: return "there are certain second components that must be taken"
        case 2: return "must take an open second component"
        default: return "must take second component with class number " + c.rel_1
      }
    } else {
      switch(c.rel_1) {
        case 0: return ""
        case 99: return "this is an open second component"
        default: return "must take primary component with class number " + c.rel_1
      }
    }
  };

  const getRelated2Note = c => {
    if (c.section_number.charAt(0) === '0') {
      switch(c.rel_2) {
        case 0: return ""
        case 1: return "there are certain third components that must be taken"
        case 2: return "must take an open third component"
        default: return "must take third component with class number " + c.rel_2
      }
    } else {
      switch(c.rel_1) {
        case 0: return ""
        case 99: return "this is an open third component"
        default: return "must take primary component with class number " + c.rel_2
      }
    }
  };

  // Dialog helpers
  const addRemoveVisibility = c => {
    // If class is not a lecture, then add/remove is not visible.
    if (c.section_number.charAt(0) !== '0') {
      return {display: 'none'};
    }
  };

  // Remove Dialog
  const handleRemoveClose = () => {
    setRemoveOpen(false);
    setClassSelected(null);
  };

  const initRemoveDialog = c => {
    if (c.rel_1 === 0 && c.rel_2 === 0) {
      removeClassFromUserSchedule(c.id);
      return;
    }
    setClassSelected(c);
    if (c.rel_1 !== 0 && c.rel_2 !== 0) {
      setDialogTitle('Remove second and third components?');
      setDialogText('The class you are about to remove has a second and third related component which will also be removed. '
        + 'Are you sure you want to remove this class?');
    } else if (c.rel_1 !== 0) {
      setDialogTitle('Remove second component');
      setDialogText('The class you are about to remove has a second related component which will also be removed. '
        + 'Are you sure you want to remove this class?');
    } else if (c.rel_2 !== 0) {
      setDialogTitle('Remove third component');
      setDialogText('The class you are about to remove has a third related component which will also be removed. '
        + 'Are you sure you want to remove this class?');
    }
    setRemoveOpen(true);
  };

  const handleRemove = () => {
    if (classSelected) {
      // Remove any classes in user's schedule that have a matching subject and catalog number (including itself)
      userClasses.map(c => {
        if (c.subject === classSelected.subject && c.catalog_number === classSelected.catalog_number) {
          removeClassFromUserSchedule(c.id);
        }
      });
    }
    setRemoveOpen(false);
    setClassSelected(null);
  };

  // Add Dialog
  const handleAddClose = () => {
    setAddOpen(false);
    setClassSelected(null);
    setRel1Value(0);
    setRel2Value(0);
  };

  const initAddDialog = c => {
    if (c.rel_1 === 0 && c.rel_2 === 0) {
      addClassToUserSchedule(c.id);
      return;
    }
    setClassSelected(c);
    setDialogTitle('Warning: related components');
    // Get all classes that match subject and catalog_number
    var matchingClasses = addableClasses.filter(d => {
      if (d.subject === c.subject && d.catalog_number === c.catalog_number) return true;
      return false;
    });
    if (c.rel_1 !== 0) {
      setShowRel1({display: 'block'});
      initRelated1(c, matchingClasses);
    } 
    if (c.rel_2 !== 0) {
      setShowRel2({display: 'block'});
      initRelated2(c, matchingClasses);
    }
    setAddOpen(true);
  };

  const initRelated1 = (c, classes) => {
    var comps = classes.filter(d => {
      if (d.section_number.charAt(0) === '1') return true;
      return false;
    });
    if (c.rel_1 === 1) {
      // Show specific second components
      comps = comps.filter(d => {
        if (d.rel_1 === c.id) return true;
        return false;
      });
    } else if (c.rel_1 !== 2) {
      // Show one specific second component
      comps = comps.filter(d => {
        if (d.id === c.rel_1) return true;
        return false;
      });
    }
    setRel1Value(comps[0].id);
    setAllowedRel1(comps);
  };

  const initRelated2 = (c, classes) => {
    var comps = classes.filter(d => {
      if (d.section_number.charAt(0) === '2') return true;
      return false;
    });
    if (c.rel_2 === 1) {
      // Show specific third components
      comps = comps.filter(d => {
        if (d.rel_1 === c.id) return true;
        return false;
      });
    } else if (c.rel_2 !== 2) {
      // Show one specific third component
      comps = comps.filter(d => {
        if (d.id === c.rel_2) return true;
        return false;
      });
    }
    setRel2Value(comps[0].id);
    setAllowedRel2(comps);
  };

  const getComponentDialogLabel = c => {
    var label = c.class_type + ' ' + c.section_number + '\n';
    label += c.weekdays + ' ' + c.start_time + ' ' + c.end_time + '\n';
    label += c.building + ' ' + c.room + '\n';
    return label;
  };

  const handleRel1Change = event => {
    setRel1Value(event.target.value);
  };

  const handleRel2Change = event => {
    setRel2Value(event.target.value);
  };

  const handleAdd = () => {
    if (classSelected) {
      addClassToUserSchedule(classSelected.id);
      if (rel1Value !== 0) {
        addClassToUserSchedule(rel1Value);
      }
      if (rel2Value !== 0) {
        addClassToUserSchedule(rel2Value);
      }
    }
    setAddOpen(false);
    setClassSelected(null);
    setRel1Value(0);
    setRel2Value(0);
  };

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
                    {`${c.id} - ${c.subject} ${c.catalog_number} - ${c.class_type} ${c.section_number}`}
                  </Typography>
                  <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                    {`${c.weekdays} ${c.start_time} ${c.end_time}`}
                  </Typography>
                  <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                    {`${c.building} ${c.room}, Campus: ${c.campus}`}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Button color="primary" onClick={() => initRemoveDialog(c)} style={addRemoveVisibility(c)}> Remove from schedule </Button>
                  <Dialog open={removeOpen} onClose={handleRemoveClose}>
                    <DialogTitle>
                      {dialogTitle}
                    </DialogTitle>
                    <DialogContent>
                      <DialogContentText>
                        {dialogText}
                      </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                      <Button onClick={handleRemove} color="primary" autoFocus>
                        Yes
                      </Button>
                    </DialogActions>
                  </Dialog>
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
          var rel1_note = getRelated1Note(c);
          var rel2_note = getRelated2Note(c);
          if (c.section_number.charAt(0) === '1') {
            rel2_note = "";
          }
          if (c.section_number.charAt(0) === '2') {
            rel1_note = "";
          }
          return (
            <ListItem component="div" key={c.id}>
              <Grid container>
                <Grid item xs={6}>
                  <Typography component="div" variant="h6" color="textPrimary" gutterBottom>
                    {`${c.id} - ${c.subject} ${c.catalog_number} - ${c.class_type} ${c.section_number}`}
                  </Typography>
                  <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                    {`${c.weekdays} ${c.start_time} ${c.end_time}`}
                  </Typography>
                  <Typography component="div" variant="body1" color="textPrimary" gutterBottom>
                    {`${c.building} ${c.room}`}
                  </Typography>
                  {
                    (rel1_note) ? 
                      <Typography component="div" variant="body2" color="textPrimary"
                      style={{fontStyle: "italic"}} gutterBottom>
                        Note: {rel1_note}
                      </Typography>
                    : null
                  }
                  {
                    (rel2_note) ? 
                      <Typography component="div" variant="body2" color="textPrimary"
                      style={{fontStyle: "italic"}} gutterBottom>
                        Note: {rel2_note}
                      </Typography>
                    : null
                  }
                </Grid>
                <Grid item xs={6}>
                  <Button color="primary" onClick={() => initAddDialog(c)} style={addRemoveVisibility(c)}> Add to schedule </Button>
                </Grid>
              </Grid>
            </ListItem>
          )
        })}
      </List>
      <Dialog open={addOpen} onClose={handleAddClose}>
        <DialogTitle>
          {dialogTitle}
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            {(allowedRel1.length === 1) ? 'The following second component will be added' : 'Please choose a second component'}
          </DialogContentText>
          <RadioGroup aria-label="rel1" name="rel1" value={rel1Value.toString()} onChange={handleRel1Change} style={showRel1}>
            {allowedRel1.map(c => {
              return (<FormControlLabel key={c.id} value={c.id.toString()} control={<Radio />}
                label={getComponentDialogLabel(c)} style={{whiteSpace: "pre-wrap"}}/>
              )
            })}
          </RadioGroup>
          <DialogContentText style={showRel2}>
          {(allowedRel2.length === 1) ? 'The following third component will be added' : 'Please choose a third component'}
          </DialogContentText>
          <RadioGroup aria-label="rel2" name="rel2" value={rel2Value.toString()} onChange={handleRel2Change} style={showRel2}>
            {allowedRel2.map(c => {
              return (<FormControlLabel key={c.id} value={c.id.toString()} control={<Radio />}
                label={getComponentDialogLabel(c)} style={{whiteSpace: "pre-wrap"}}/>
              )
            })}
          </RadioGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleAdd} color="primary" autoFocus>
            Done
          </Button>
        </DialogActions>
      </Dialog>
    </>
  )
}

export default MainPage;