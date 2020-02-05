import React from 'react';
import ClassList from './classList';
import TimeSelect from './timeSelect';


function ClassSearch({ classes, setClasses }: props) {
    return (
        <div>
            <div style={{marginBottom: "20px"}}>
                <TimeSelect setClasses={setClasses}/>
            </div>
            <ClassList classes={classes}/>
        </div>
    )
}

export default ClassSearch;