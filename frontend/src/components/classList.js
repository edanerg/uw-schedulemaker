import React, { useState } from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

function ClassList(props) {
    const [hoveredClassId, setHoveredClassId] = useState(null)

    const mouseEnter = id => {
        setHoveredClassId(id)
    }

    const mouseExit = () => {
        setHoveredClassId(null)
    }

    return (
        <div>
            {(props.classes || []).map(c => 
                <Card key={c.id} style={{marginBottom: "10px", cursor: "pointer"}} raised={hoveredClassId === c.id}
                    onMouseEnter={() => mouseEnter(c.id)}
                    onMouseLeave={mouseExit}>
                    <CardContent>
                        <Typography variant="h5" color="textPrimary">
                            {`${c.subject} ${c.catalog_number} ${c.name}`}
                        </Typography>
                        <Typography variant="body1" color="textSecondary">
                            {`${c.building} ${c.room}`}
                        </Typography>
                        <Typography variant="body1" color="textSecondary">
                            {`${c.weekdays} ${c.start_time}-${c.end_time}`}
                        </Typography>
                        <Typography variant="body1" color="textSecondary">
                            {c.description}
                        </Typography>
                    </CardContent>
                </Card>
            )}
        </div>
    )
}

export default ClassList;
