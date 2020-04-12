import React, { useState, useEffect } from 'react';
import ClassList from './classList';
import {TextField, Button} from '@material-ui/core';
import serverURL from '../config';
import axios from 'axios';


function InstructorSearch({ classes, setClasses }: props) {
    const [instructorname, setinstructorname] = useState("");
    const refresh = () => {
        axios.get(`${serverURL}/instructor`, {params: 
            {instructor: instructorname}})
            .then(res => setClasses(res.data.classes));
    }
    return (
        <div>
            <div style={{marginBottom: "20px"}}>
                <TextField type="text" name="Instructor name" placeholder="Instructor name" onChange={text => setinstructorname(text.target.value)}/>
                <Button variant="contained" color="primary" onClick={refresh} style={{marginLeft: "10px"}}>Search</Button>
            </div>
            <ClassList classes={classes}/>
        </div>
    )
}

export default InstructorSearch;