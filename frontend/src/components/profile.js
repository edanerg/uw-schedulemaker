import React, {useState} from 'react';
import CoursesList from './coursesList';
import { subjects } from './coursesSearch';
import { Button, ButtonGroup, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Select from 'react-select'
import {TextField} from '@material-ui/core';
import axios from 'axios';
import serverURL from '../config';

const useStyles = makeStyles(theme => ({
  button: {
    marginRight: theme.spacing(2),
  },
  courseContainer: {
    display: "flex",
    marginBottom: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
  selectBox: {
    width: '200px',
    marginRight: theme.spacing(2),
  }
}));

function Profile({user, coursesTaken, setCoursesTaken}) {
  const classes = useStyles();
  const [subject, setSubject] = useState("CS");
  const [catalog, setCatalog] = useState(null);
  const [msg, setMsg] = useState(null);

  const uploadCourse = () => {
    axios.post(`${serverURL}/coursesTaken`, {
      username: user.username,
      subject,
      catalog_number: catalog
    }).then(res => {
      if (res.data.result != 'success') {
        setMsg(res.data.result)
      } else {
        setMsg("Course successfully added")
        const courses = [...coursesTaken]
        courses.push(res.data.course)
        setCoursesTaken(courses)
      } 
    })
  }

  const deleteCourse = () => {
    const params = {
      username: user.username,
      subject,
      catalog_number: catalog
    }
    axios.delete(`${serverURL}/coursesTaken`, {
      params
    }).then(res => {
      if (res.data.result != 'success') {
        setMsg(res.data.result)
      } else {
        setMsg("Course successfully removed")
        const courses = [...coursesTaken].filter(v => !(v.subject == params.subject && v.catalog_number == params.catalog_number))
        setCoursesTaken(courses)
      }
    })
  }
  return (
    <div style={{display: "flex", flexDirection: "column", justifyContent: "flex-start", alignItems: "start"}}>
      <Typography variant="h4" gutterBottom>{user.username}</Typography>
      <Typography variant="h5" gutterBottom>{`Academic level: ${user.academic_level}`}</Typography>
      <Typography variant="h5" gutterBottom>Courses you took</Typography>
      <CoursesList courses={coursesTaken}/>
      <div className={classes.courseContainer} >
        <div className={classes.selectBox} >
          <Select
            options={subjects}
            onChange={option => setSubject(option != null ? option.value : null)}
            isSearchable={true}
            isClearable={true}
            placeholder={subject}
            />
        </div>
        <div className={classes.button} >
            <TextField type="text" name="catalog" placeholder="Course code" onChange={text => setCatalog(text.target.value)}/>
        </div>
        <ButtonGroup>
          <Button className={classes.button} onClick={uploadCourse} variant="contained" color="primary">Add Course</Button>
          <Button className={classes.button} onClick={deleteCourse} variant="contained" color="primary">Delete Course</Button>
        </ButtonGroup>
      </div>
      <span style={{color: "red"}} >{msg}</span>
    </div>
  )
}

export default Profile;