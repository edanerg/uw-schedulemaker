import React, { useState } from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

function ClassList({ classes }: props) {
    const [hoveredClassId, setHoveredClassId] = useState(null)

    const mouseEnter = id => {
        setHoveredClassId(id)
    }

    const mouseExit = () => {
        setHoveredClassId(null)
    }

    return (
        <div>
            {(classes || []).map((c, index) => 
                <Card key={index} style={{marginBottom: "10px", cursor: "pointer"}} raised={hoveredClassId === index}
                    onMouseEnter={() => mouseEnter(c.id)}
                    onMouseLeave={mouseExit}>
                    <CardContent>
                        <Typography variant="h5" color="textPrimary">
                            {`${c.subject} ${c.catalog_number} ${c.name || ""}`}
                        </Typography>
                        <Typography variant="h5" color="textSecondary">
                            {`${c.weekdays} ${c.start_time}-${c.end_time}`}
                        </Typography>
                        <Typography variant="h5" color="textSecondary">
                            {`Section: ${c.class_type} ${c.section_number}`}
                        </Typography>
                    </CardContent>
                    <ExpansionPanel>
                      <ExpansionPanelSummary
                        expandIcon={<ExpandMoreIcon />}
                      >
                        <Typography variant="body1" color="textSecondary">More info</Typography>
                      </ExpansionPanelSummary>
                      <ExpansionPanelDetails style={{ flexDirection: "column" }}>
                        <Typography variant="body1" color="textPrimary" gutterBottom>
                          Description
                        </Typography>
                        <Typography variant="body1" color="textSecondary" gutterBottom>
                          {c.description}
                        </Typography>
                        <Typography variant="body1" color="textPrimary" gutterBottom>
                          Location
                        </Typography>
                        <Typography variant="body1" color="textSecondary" gutterBottom>
                          {`${c.building} ${c.room}`}
                        </Typography>
                        <Typography variant="body1" color="textPrimary" gutterBottom>
                          Instructor
                        </Typography>
                        <Typography variant="body1" color="textSecondary" gutterBottom>
                          {(c.instructor) ? `${c.instructor}` : "TBA"}
                        </Typography>
                      </ExpansionPanelDetails>
                    </ExpansionPanel>
                </Card>
            )}
        </div>
    )
}

export default ClassList;
