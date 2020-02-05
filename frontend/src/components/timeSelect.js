import React, { useState, useEffect } from 'react';
import Grid from '@material-ui/core/Grid';
import 'date-fns';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
} from '@material-ui/pickers';
import { FormControl,
         FormControlLabel,
         Checkbox,
         Fab} from '@material-ui/core';
import RefreshIcon from '@material-ui/icons/Refresh';
import serverURL from '../config';
import axios from 'axios';

const defaultSelectedDays = {M: false, T: false, W: false, Th: false, F: false};
function TimeSelect({ setClasses }: props) {

    const [selectedDays, setSelectedDays] = useState(defaultSelectedDays);
    const [startTime, setStartTime] = useState(null);
    const [endTime, setEndTime] = useState(null);

    useEffect(() => {
      axios.get(`${serverURL}/class`, {params: 
        {weekdays: Object.keys(selectedDays).filter(k => selectedDays[k]).join(""),
        from_time: startTime ? startTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false}) : undefined,
        to_time: endTime ? endTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', hour12: false}) : undefined}})
        .then(res => setClasses(res.data.classes));
    }, [setClasses, selectedDays, startTime, endTime]);

    const resetSearch = () => {
      setSelectedDays(defaultSelectedDays);
      setStartTime(null);
      setEndTime(null);
    }

    return (
        <MuiPickersUtilsProvider utils={DateFnsUtils}>
            <Grid container justify="space-around" alignItems="center">
                <FormControl style={{marginTop: "30px", display: 'flex', flexDirection: 'row'}}>
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
                    margin="normal"
                    id="start-time-picker"
                    label="Start Time"
                    value={startTime}
                    onChange={setStartTime}
                    KeyboardButtonProps={{
                        'aria-label': 'start time',
                    }}
                    style={{width: "180px"}}
                />
                <KeyboardTimePicker
                    margin="normal"
                    id="end-time-picker"
                    label="End Time"
                    value={endTime}
                    onChange={setEndTime}
                    KeyboardButtonProps={{
                        'aria-label': 'end time',
                    }}
                    style={{width: "180px"}}
                />
                <Fab color="primary" size="small" style={{marginTop: "20px"}} onClick={resetSearch}><RefreshIcon /></Fab>
            </Grid>
        </MuiPickersUtilsProvider>
    )
}

export default TimeSelect;