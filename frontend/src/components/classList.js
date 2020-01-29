import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

/* 
    TODO: don't hard code, use query results
 */
const defaultCourses = [
    {   id: "1",
        name: "JJ101",
        time: "MWF 9:00-10:20",
        instructor: "Kujo Jotaro",
        location: "Egypt"
    },
    {   id: "2",
        name: "JJ201",
        time: "F 19:00-21:00",
        instructor: "Johny Jostar",
        location: "The Wild Wacky West"
    },
    {   id: "3",
        name: "JJ301",
        time: "M 19:00-21:00",
        instructor: "Jonathon Jostar",
        location: "Some Ramdom English Mansion"
    },
    {   id: "4",
        name: "JJ401",
        time: "MW 12:00-13:30",
        instructor: "Higashikata Josuke",
        location: "Morioh"
    }]


class ClassList extends Component {

    state = {
        courses: defaultCourses,
        hoveredCourseId: null
    }

    mouseEnter = id => {
        this.setState({
            hoveredCourseId: id
        })
    }

    mouseExit = () => {
        this.setState({
            hoveredCourseId: null
        })
    }

    render() {
        return (
            <div>
                {this.state.courses.map(c => 
                    <Card key={c.id} style={{marginBottom: "10px", cursor: "pointer"}} raised={this.state.hoveredCourseId === c.id}
                        onMouseEnter={this.mouseEnter.bind(this, c.id)}
                        onMouseLeave={this.mouseExit}>
                        <CardContent>
                            <Typography variant="h5" color="textPrimary" component="h2">
                                {c.name}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="p">
                                {c.time}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="p">
                                {c.instructor}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="p">
                                {c.location}
                            </Typography>
                        </CardContent>
                    </Card>
                )}
            </div>
        )
    }
}

export default ClassList;