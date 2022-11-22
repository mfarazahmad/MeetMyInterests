/* eslint-disable @next/next/no-img-element */
import React, { useEffect, useRef } from 'react'
import styles from '../styles/Home.module.css'

import Outline from '../components/Layout/Outline'
import { LoginContext } from '../context/ctx'

const Dashboard = (props) => {

    return (
        <LoginContext.Consumer >
            {value =>
                <div>
                    {value.isLoggedIn ? (
                        <Outline>
                            <div className={styles.main}>
                                TEST
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

export default Dashboard;