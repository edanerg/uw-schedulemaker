import React, { useState, useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import 'date-fns';
import Select from 'react-select'
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
} from '@material-ui/pickers';
import { FormControl,
         FormControlLabel,
         Checkbox,
         TextField,
         Fab} from '@material-ui/core';
import RefreshIcon from '@material-ui/icons/Refresh';
import serverURL from '../config';
import axios from 'axios';
import { subjects } from './coursesSearch';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  flexDisplay: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
    display: 'flex',
    flexDirection: 'row'
  },
  margin: {
    margin: theme.spacing(2),
  },
  selectSubject: {
    margin: theme.spacing(2),
    width: '150px',
  },
}));

const defaultSelectedDays = {M: false, T: false, W: false, Th: false, F: false};
const defaultCourse = 'CS';

function TimeSelect({ setClasses }: props) {
    const classes = useStyles();
    const [selectedDays, setSelectedDays] = useState(defaultSelectedDays);
    const [startTime, setStartTime] = useState(null);
    const [endTime, setEndTime] = useState(null);
    const [subject, setSubject] = useState(defaultCourse);
    const [catalog, setCatalog] = useState(null);

    useEffect(() => {
      axios.get(`${serverURL}/class`, {params: 
        {weekdays: Object.keys(selectedDays).filter(k => selectedDays[k]).join(""),
        from_time: startTime ? startTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false}) : undefined,
        to_time: endTime ? endTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false}) : undefined,
        subject: subject,
        catalog_number: catalog,
        }})
        .then(res => setClasses(res.data.classes));
    }, [setClasses, subject, catalog, selectedDays, startTime, endTime]);

    const resetSearch = () => {
      setSelectedDays(defaultSelectedDays);
      setStartTime(null);
      setEndTime(null);
      setSubject(defaultCourse);
      setCatalog(null);
    }

    return (
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
          <Grid className={classes.flexDisplay}>
              <FormControl className={classes.flexDisplay}>
                  <FormControlLabel
                  value="M"
                  control={<Checkbox color="primary" size="small" onChange={e => setSelectedDays({...selectedDays, M:e.target.checked})}/>}
                  label="M"
                  labelPlacement="bottom"
                  />
                  <FormControlLabel
                  value="T"
                  control={<Checkbox color="primary" size="small" onChange={e => setSelectedDays({...selectedDays, T:e.target.checked})}/>}
                  label="T"
                  labelPlacement="bottom"
                  />
                  <FormControlLabel
                  value="W"
                  control={<Checkbox color="primary" size="small" onChange={e => setSelectedDays({...selectedDays, W:e.target.checked})}/>}
                  label="W"
                  labelPlacement="bottom"
                  />
                  <FormControlLabel
                  value="Th"
                  control={<Checkbox color="primary" size="small" onChange={e => setSelectedDays({...selectedDays, Th:e.target.checked})}/>}
                  label="Th"
                  labelPlacement="bottom"
                  />
                  <FormControlLabel
                  value="F"
                  control={<Checkbox color="primary" size="small" onChange={e => setSelectedDays({...selectedDays, F:e.target.checked})}/>}
                  label="F"
                  labelPlacement="bottom"
                  />
              </FormControl>
              <KeyboardTimePicker
                  className={classes.timePicker}
                  margin="normal"
                  id="start-time-picker"
                  label="Start Time"
                  value={startTime}
                  onChange={setStartTime}
                  style={{width: "180px"}}
              />
              <KeyboardTimePicker
                  className={classes.margin}
                  margin="normal"
                  id="end-time-picker"
                  label="End Time"
                  value={endTime}
                  onChange={setEndTime}
                  style={{width: "180px"}}
              />
              <Select
                className={classes.selectSubject}
                options={subjects}
                onChange={option => setSubject(option != null ? option.value : null)}
                isSearchable={true}
                isClearable={true}
                placeholder={subject}
              />
              <TextField
                className={classes.selectSubject}
                type="text"
                name="catalog"
                placeholder="Course code"
                onChange={text => setCatalog(text.target.value)}
              />
              <Fab
                className={classes.margin}
                color="primary"
                size="small"
                onClick={resetSearch}
              ><RefreshIcon /></Fab>
          </Grid>
        </MuiPickersUtilsProvider>
    )
}

export default TimeSelect;