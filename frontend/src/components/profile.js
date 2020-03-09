import React, {useState} from 'react';
import CoursesList from './coursesList';
import { subjects } from './coursesSearch';
import { Button } from '@material-ui/core';
import Select from 'react-select'
import {TextField} from '@material-ui/core';
import axios from 'axios';
import serverURL from '../config';

function Profile({user, coursesTaken, setCoursesTaken}) {

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
      <div style={{fontSize: "40px", marginBottom: "5px"}}>{user.username}</div>
      <div style={{fontSize: "30px", marginBottom: "20px"}}>Courses Taken</div>
      <CoursesList courses={coursesTaken}/>
      <div>
            <div style={{width: '200px', display: "inline-block", marginRight: '100px', marginBottom: '60px'}}>
              <Select
                options={subjects}
                onChange={option => setSubject(option != null ? option.value : null)}
                isSearchable={true}
                isClearable={true}
                placeholder={subject}
                />
            </div>
            <div style={{display: "inline-block"}}>
                <TextField type="text" name="catalog" placeholder="Course code" onChange={text => setCatalog(text.target.value)}/>
            </div>
      </div>

      <Button style={{marginBottom: "10px"}} onClick={uploadCourse} variant="contained" color="primary">Add Course</Button>
      <Button style={{marginBottom: "5px"}} onClick={deleteCourse} variant="contained" color="primary">Delete Course</Button>
      <span style={{color: "red"}} >{msg}</span>
    </div>
  )
}

export default Profile;