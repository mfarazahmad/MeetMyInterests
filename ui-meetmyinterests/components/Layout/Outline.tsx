import React from 'react'
import Navbar from './Navbar'
import { LoginContext } from '../../context/ctx'

type Props = {
    children: JSX.Element
}

const Outline = (props: Props) => {

    return (
        <div className="outline">
            <LoginContext.Consumer >
                {value =>
                    <Navbar
                        showLoginBox={value.showLoginBox}
                        handleLoginDisplay={value.handleLoginDisplay}
                        isLoggedIn={value.isLoggedIn}
                        handleLogin={value.handleLogin}
                        handleLogout={value.handleLogout} />
                }
            </LoginContext.Consumer>
            {props.children}
        </div>
    )
}

export default Outline;