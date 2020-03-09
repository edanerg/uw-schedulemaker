import React, { useState } from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

function CoursesList({ courses } : props) {
    const [hoveredClassId, setHoveredClassId] = useState(null)

    const mouseEnter = id => {
        setHoveredClassId(id)
    }

    const mouseExit = () => {
        setHoveredClassId(null)
    }

    return (
        <div>
            {courses.length ?
              courses.map(c => {
              const key = `${c.subject}${c.catalog_number}`
              return (
                <Card key={key} style={{marginBottom: "10px", cursor: "pointer"}} raised={hoveredClassId === key}
                    onMouseEnter={() => mouseEnter(key)}
                    onMouseLeave={mouseExit}>
                    <CardContent>
                        <Typography variant="h5" color="textPrimary">
                            {`${c.subject} ${c.catalog_number}: ${c.name}`}
                        </Typography>
                        <Typography variant="body1" color="textSecondary">
                            {c.description}
                        </Typography>
                        <Typography variant="body1" color="textSecondary">
                            {c.prerequisites && `Prerequisites : ${c.prerequisites}`}
                        </Typography>
                        <Typography variant="body1" color="textSecondary">
                             {c.antirequisites && `Antirequisites : ${c.antirequisites}`}
                        </Typography>
                    </CardContent>
                </Card>
              )
            })
            : 
            <Typography variant="h5" color="textPrimary">
              No Courses found 
            </Typography>
          }
        </div>
    )
}

export default CoursesList;
