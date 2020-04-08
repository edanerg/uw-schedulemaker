import React, { useState, useEffect } from 'react';
import Select from 'react-select'
import {TextField} from '@material-ui/core';
import CoursesList from './coursesList';
import serverURL from '../config';
import axios from 'axios';

export const subjects = [
    { value: 'ACC', label: 'ACC' }, { value: 'ACINTY', label: 'ACINTY' }, { value: 'ACTSC', label: 'ACTSC' }, { value: 'AFM', label: 'AFM' },
    { value: 'AHS', label: 'AHS' }, { value: 'AMATH', label: 'AMATH' }, { value: 'ANTH', label: 'ANTH' }, { value: 'APPLS', label: 'APPLS' },
    { value: 'ARBUS', label: 'ARBUS' }, { value: 'ARCH', label: 'ARCH' }, { value: 'ARCHL', label: 'ARCHL' }, { value: 'ARTS', label: 'ARTS' },
    { value: 'ASL', label: 'ASL' }, { value: 'ASTRN', label: 'ASTRN' }, { value: 'AVIA', label: 'AVIA' }, { value: 'BASE', label: 'BASE' },
    { value: 'BE', label: 'BE' }, { value: 'BET', label: 'BET' }, { value: 'BIOL', label: 'BIOL' }, { value: 'BME', label: 'BME' },
    { value: 'BUS', label: 'BUS' }, { value: 'CDNST', label: 'CDNST' }, { value: 'CHE', label: 'CHE' }, { value: 'CHEM', label: 'CHEM' },
    { value: 'CHINA', label: 'CHINA' }, { value: 'CI', label: 'CI' }, { value: 'CIVE', label: 'CIVE' }, { value: 'CLAS', label: 'CLAS' },
    { value: 'CM', label: 'CM' }, { value: 'CMW', label: 'CMW' }, { value: 'CO', label: 'CO' }, { value: 'COGSCI', label: 'COGSCI' },
    { value: 'COMM', label: 'COMM' }, { value: 'COOP', label: 'COOP' }, { value: 'CRGC', label: 'CRGC' }, { value: 'CROAT', label: 'CROAT' },
    { value: 'CS', label: 'CS' }, { value: 'CT', label: 'CT' }, { value: 'CULT', label: 'CULT' }, { value: 'DAC', label: 'DAC' },
    { value: 'DEI', label: 'DEI' }, { value: 'DRAMA', label: 'DRAMA' }, { value: 'DUTCH', label: 'DUTCH' }, { value: 'EARTH', label: 'EARTH' },
    { value: 'EASIA', label: 'EASIA' }, { value: 'ECDEV', label: 'ECDEV' }, { value: 'ECE', label: 'ECE' }, { value: 'ECON', label: 'ECON' },
    { value: 'EDMI', label: 'EDMI' }, { value: 'EFAS', label: 'EFAS' }, { value: 'ELPE', label: 'ELPE' }, { value: 'EMLS', label: 'EMLS' },
    { value: 'ENBUS', label: 'ENBUS' }, { value: 'ENGL', label: 'ENGL' }, { value: 'ENTR', label: 'ENTR' }, { value: 'ENVE', label: 'ENVE' },
    { value: 'ENVS', label: 'ENVS' }, { value: 'ERS', label: 'ERS' }, { value: 'FINE', label: 'FINE' }, { value: 'FR', label: 'FR' },
    { value: 'GBDA', label: 'GBDA' }, { value: 'GC', label: 'GC' }, { value: 'GEMCC', label: 'GEMCC' }, { value: 'GENE', label: 'GENE' },
    { value: 'GEOE', label: 'GEOE' }, { value: 'GEOG', label: 'GEOG' }, { value: 'GER', label: 'GER' }, { value: 'GERON', label: 'GERON' },
    { value: 'GESC', label: 'GESC' }, { value: 'GGOV', label: 'GGOV' }, { value: 'GLOBAL', label: 'GLOBAL' }, { value: 'GRK', label: 'GRK' },
    { value: 'GS', label: 'GS' }, { value: 'GSJ', label: 'GSJ' }, { value: 'HESC', label: 'HESC' }, { value: 'HIST', label: 'HIST' },
    { value: 'HLTH', label: 'HLTH' }, { value: 'HRM', label: 'HRM' }, { value: 'HRTS', label: 'HRTS' }, { value: 'HUMSC', label: 'HUMSC' },
    { value: 'INDEV', label: 'INDEV' }, { value: 'INDG', label: 'INDG' }, { value: 'INTEG', label: 'INTEG' }, { value: 'INTST', label: 'INTST' },
    { value: 'ITAL', label: 'ITAL' }, { value: 'ITALST', label: 'ITALST' }, { value: 'JAPAN', label: 'JAPAN' }, { value: 'JS', label: 'JS' },
    { value: 'KIN', label: 'KIN' }, { value: 'KOREA', label: 'KOREA' }, { value: 'KPE', label: 'KPE' }, { value: 'LANG', label: 'LANG' },
    { value: 'LAT', label: 'LAT' }, { value: 'LS', label: 'LS' }, { value: 'MATBUS', label: 'MATBUS' }, { value: 'MATH', label: 'MATH' },
    { value: 'ME', label: 'ME' }, { value: 'MEDVL', label: 'MEDVL' }, { value: 'MGMT', label: 'MGMT' }, { value: 'MISC', label: 'MISC' },
    { value: 'MNS', label: 'MNS' }, { value: 'MOHAWK', label: 'MOHAWK' }, { value: 'MSCI', label: 'MSCI' }, { value: 'MTE', label: 'MTE' },
    { value: 'MTHEL', label: 'MTHEL' }, { value: 'MUSIC', label: 'MUSIC' }, { value: 'NANO', label: 'NANO' }, { value: 'NE', label: 'NE' },
    { value: 'OLRD', label: 'OLRD' }, { value: 'OPTOM', label: 'OPTOM' }, { value: 'PACS', label: 'PACS' }, { value: 'PD', label: 'PD' },
    { value: 'PDARCH', label: 'PDARCH' }, { value: 'PDPHRM', label: 'PDPHRM' }, { value: 'PHARM', label: 'PHARM' }, { value: 'PHIL', label: 'PHIL' },
    { value: 'PHS', label: 'PHS' }, { value: 'PHYS', label: 'PHYS' }, { value: 'PLAN', label: 'PLAN' }, { value: 'PLCG', label: 'PLCG' },
    { value: 'PMATH', label: 'PMATH' }, { value: 'PORT', label: 'PORT' }, { value: 'PS', label: 'PS' }, { value: 'PSCI', label: 'PSCI' },
    { value: 'PSYCH', label: 'PSYCH' }, { value: 'QIC', label: 'QIC' }, { value: 'REC', label: 'REC' }, { value: 'REES', label: 'REES' },
    { value: 'RELC', label: 'RELC' }, { value: 'RS', label: 'RS' }, { value: 'RSCH', label: 'RSCH' }, { value: 'RUSS', label: 'RUSS' },
    { value: 'SCBUS', label: 'SCBUS' }, { value: 'SCCOM', label: 'SCCOM' }, { value: 'SCI', label: 'SCI' }, { value: 'SDS', label: 'SDS' },
    { value: 'SE', label: 'SE' }, { value: 'SEQ', label: 'SEQ' }, { value: 'SI', label: 'SI' }, { value: 'SMF', label: 'SMF' },
    { value: 'SOC', label: 'SOC' }, { value: 'SOCIN', label: 'SOCIN' }, { value: 'SOCWK', label: 'SOCWK' }, { value: 'SPAN', label: 'SPAN' },
    { value: 'SPCOM', label: 'SPCOM' }, { value: 'STAT', label: 'STAT' }, { value: 'STV', label: 'STV' }, { value: 'SUSM', label: 'SUSM' },
    { value: 'SVENT', label: 'SVENT' }, { value: 'SWK', label: 'SWK' }, { value: 'SWREN', label: 'SWREN' }, { value: 'SYDE', label: 'SYDE' },
    { value: 'TAX', label: 'TAX' }, { value: 'THPERF', label: 'THPERF' }, { value: 'TN', label: 'TN' }, { value: 'TPM', label: 'TPM' },
    { value: 'TS', label: 'TS' }, { value: 'UN', label: 'UN' }, { value: 'UNIV', label: 'UNIV' }, { value: 'UU', label: 'UU' },
    { value: 'UX', label: 'UX' }, { value: 'VCULT', label: 'VCULT' }, { value: 'WATER', label: 'WATER' }, { value: 'WHMIS', label: 'WHMIS' },
    { value: 'WKRPT', label: 'WKRPT' }, { value: 'WS', label: 'WS' },
];

const defaultCourse = 'ACC';

function CoursesSearch({ courses, setCourses }: props) {
    const [subject, setSubject] = useState(defaultCourse);
    const [catalog, setCatalog] = useState(null);

    useEffect(() => {
      axios.get(`${serverURL}/courses`, {params: 
        {subject: subject, catalog: catalog}})
        .then(res => setCourses(res.data.courses));
    }, [subject, catalog, setCourses]);

    return (
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
            <CoursesList courses={courses}/>
        </div>
    )
}

export default CoursesSearch;