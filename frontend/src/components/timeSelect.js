import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import 'date-fns';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
} from '@material-ui/pickers';
import { Select,
         Chip,
         MenuItem,
         Input,
         FormControl,
         InputLabel,
         Fab} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';


const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
const MenuProps = {
    PaperProps: {
      style: {
        width: 135,
      },
    },
};

class timeSelect extends Component {

    state = {
        selectedDays: [],
        startTime: null,
        endTime: null
    }

    startTimeChange = time => {
        this.setState({
            startTime: time
        })
    }

    endTimeChange = time => {
        this.setState({
            endTime: time
        })
    }

    selectedDaysChange = event => {
        this.setState({
            selectedDays: event.target.value
        })
    }

    search = () => {
        /* 
        TODO: call backend functions
        maybe need to add redux
         */
    }

    render() {
        /* 
        TODO: get rid of ugly inline styling
         */
        return (
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
                <Grid container justify="space-around" alignItems="center">
                    <FormControl style={{marginTop: "16px", marginBottom: "8px"}}>
                        <InputLabel id="day-picker">Day</InputLabel>
                        <Select style={{width: "250px", height: "32px"}}
                            labelId="day-picker"
                            id="day-picker"
                            multiple
                            value={this.state.selectedDays}
                            onChange={this.selectedDaysChange}
                            input={<Input id="day-select" />}
                            renderValue={selected => (
                                <div style={{display: 'flex', flexWrap: 'wrap', width: "250px"}}>
                                {selected.map(value => (
                                    <Chip key={value} label={value.substring(0, 2)} style={{margin: 1, fontSize: "14px"}} />
                                ))}
                                </div>
                            )}
                            MenuProps={MenuProps}
                            >
                            {days.map(day => (
                                <MenuItem key={day} value={day}>
                                {day}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <KeyboardTimePicker
                        margin="normal"
                        id="start-time-picker"
                        label="Start Time"
                        value={this.state.startTime}
                        onChange={this.startTimeChange}
                        KeyboardButtonProps={{
                            'aria-label': 'start time',
                        }}
                    />
                    <KeyboardTimePicker
                        margin="normal"
                        id="end-time-picker"
                        label="End Time"
                        value={this.state.endTime}
                        onChange={this.endTimeChange}
                        KeyboardButtonProps={{
                            'aria-label': 'end time',
                        }}
                    />
                    <Fab color="primary" size="small" style={{marginTop: "20px"}} onClick={this.search}><SearchIcon /></Fab>
                </Grid>
            </MuiPickersUtilsProvider>
        )
    }
}

export default timeSelect;