import React, { Component } from 'react';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

class ClassList extends Component {

    state = {
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
                {(this.props.courses || []).map(c => 
                    <Card key={c.id} style={{marginBottom: "10px", cursor: "pointer"}} raised={this.state.hoveredCourseId === c.id}
                        onMouseEnter={this.mouseEnter.bind(this, c.id)}
                        onMouseLeave={this.mouseExit}>
                        <CardContent>
                            <Typography variant="h5" color="textPrimary" component="h2">
                                {c.name}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="p">
                                {c.id}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="p">
                                {`${c.subject} ${c.catalog_number}`}
                            </Typography>
                            <Typography variant="body2" color="textSecondary" component="p">
                                {c.description}
                            </Typography>
                        </CardContent>
                    </Card>
                )}
            </div>
        )
    }
}

export default ClassList;
