/** 
 * Protect Workout Form Securely
 * Use SQL Lite for DB Entries
 * Require Google Oauth2 Login to Use
 * 
*/

import React, { useEffect, useState } from 'react';

import { Calendar } from 'antd';

import ProgramForm from '../components/Fitness/ProgramForm';
import Tracker from '../components/Fitness/Tracker';
import ProgramDisplay from '../components/Fitness/ProgramDisplay';

import { programOptions } from '../utils/constants';

import Outline from '../components/Layout/Outline'

import styles from '../styles/Fitness.module.css'
import { LoginContext } from '../context/ctx';


const Fitness = (props) => {

    const [newProgramExcercises, saveNewProgramExcercise] = useState([]);
    const [programsInfo, setProgramInfo] = useState([]);

    const [isProgramVisible, setProgramVisibility] = useState(false);
    const [isexcerciseProgramVisible, setExcerciseProgramVisibility] = useState(true);

    useEffect(() => {
        console.log(programsInfo);
    }, [programsInfo])

    const onPanelChange = (value) => console.log(value);
    const handleForm = (values, formType) => {
        const data = [];

        if (formType === 'program') {
            const updatedPrograms = programsInfo;
            values['id'] = programOptions.length + 1;
            values['programExcercises'] = newProgramExcercises;

            // Update UI to Reflect New Program
            updatedPrograms.push(values);
            programOptions.push({ label: values['programName'], value: values['id'] });

            setProgramInfo(updatedPrograms);
            toggleProgramForm();
            console.log(programsInfo);
        } else if (formType === 'programExcercise') {
            let newExcercises = newProgramExcercises;
            newExcercises.push(values);
            saveNewProgramExcercise(newExcercises);
            toggleExcerciseProgramForm();
            console.log(newProgramExcercises);
        }


    }

    const toggleProgramForm = () => {
        saveNewProgramExcercise([]);
        setProgramVisibility((isProgramVisible) => !isProgramVisible);
    }
    const toggleExcerciseProgramForm = () => setExcerciseProgramVisibility((isexcerciseProgramVisible) => !isexcerciseProgramVisible);

    return (

        <LoginContext.Consumer >
            {value =>
                <div>
                    {!value.isLoggedIn ? (
                        <Outline>
                            <div className={styles.container}>
                                <h1>Fitness Tracker</h1>
                                <Calendar
                                    onPanelChange={onPanelChange}
                                />
                                <ProgramForm handleForm={handleForm}
                                    isProgramVisible={isProgramVisible}
                                    isexcerciseProgramVisible={isexcerciseProgramVisible}
                                    toggleProgramForm={toggleProgramForm}
                                    toggleExcerciseProgramForm={toggleExcerciseProgramForm}
                                    newProgramExcercises={newProgramExcercises}
                                />
                                <ProgramDisplay
                                    programsInfo={programsInfo}
                                    toggleProgramForm={toggleProgramForm}
                                />
                                <Tracker />
                            </div>
                        </Outline>
                    ) :
                        (<div>NOT AUTHORIZED TO VIEW THIS PAGE</div>)
                    }
                </div>
            }
        </LoginContext.Consumer>
    )
}

export default Fitness;