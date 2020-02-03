import React, {Component} from 'react';
import ClassList from './classList';
import TimeSelect from './timeSelect';


class ClassSearch extends Component {
    render () {
        return (
            <div>
                <div style={{marginBottom: "20px"}}>
                    <TimeSelect setCourses={this.props.setCourses}/>
                </div>
                <ClassList courses={this.props.courses}/>
            </div>
        )
    }
}

export default ClassSearch;