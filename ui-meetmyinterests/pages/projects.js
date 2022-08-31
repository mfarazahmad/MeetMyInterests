import React, { useState, useEffect } from 'react'

import styles from '../styles/Projects.module.css'
import Outline from '../components/Layout/Outline'
import AboutMe from '../components/Projects/AboutMe'
import ProjectShowCase from '../components/Projects/ProjectShowCase'

const Projects = (props) => {

    return (
        <Outline>
            <div className={styles.main}>
                <h1 className={styles.header} id="aboutMeBanner"> About Me </h1>
                <AboutMe />

                <h1 className={styles.header}> Projects </h1>
                <ProjectShowCase />
            </div>
        </Outline>
    )
}

export default Projects