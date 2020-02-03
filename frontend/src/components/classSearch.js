import React from 'react';
import ClassList from './classList';
import TimeSelect from './timeSelect';


function ClassSearch(props) {
    return (
        <div>
            <div style={{marginBottom: "20px"}}>
                <TimeSelect setClasses={props.setClasses}/>
            </div>
            <ClassList classes={props.classes}/>
        </div>
    )
}

export default ClassSearch;