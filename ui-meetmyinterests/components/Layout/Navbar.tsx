/* eslint-disable @next/next/no-img-element */
import React, { MouseEventHandler, useState } from 'react'
import Link from 'next/link'

import { Avatar, Badge, Button } from 'antd'

import Login from '../Auth/Login'
import Logout from '../Auth/Logout'

type Props = {
    isLoggedIn: boolean,
    handleLogin: MouseEventHandler<HTMLElement>,
    handleLogout: MouseEventHandler<HTMLElement>,
}

const Navbar = (props: Props) => {

    const [showLoginBox, setLoginDisplay] = useState(false)

    const handleLoginDisplay = () => {
        setLoginDisplay((showLoginBox) => !showLoginBox)
    }

    return (
        <div className="navbar">
            <div className='welcomeMsg'>
                <div>
                    Welcome, Faraz
                </div>
                <div>
                    <Badge count={1}>
                        <Link href="/dash" passHref>
                            <Avatar style={{ backgroundColor: 'red', verticalAlign: 'middle' }} shape="square" size="large" gap={5}>
                                Dash
                            </Avatar>
                        </Link>
                    </Badge>
                </div>
            </div>

            {showLoginBox && <Login handleLoginDisplay={handleLoginDisplay} handleLogin={props.handleLogin} />}

            {!props.isLoggedIn ?
                (
                    <div>
                        <Button className='loginBtn' onClick={handleLoginDisplay}>Login</Button>
                    </div>
                ) :
                (
                    <div>
                        <Logout handleLogout={props.handleLogout} />
                    </div>
                )
            }

            <div className='linkTags'>
                <Link href="/"><a>Home</a></Link>
                <Link href="/projects"><a>Projects</a></Link>
                <Link href="/blog"><a>Blog</a></Link>
                <Link href="/fitness"><a>Fitness</a></Link>
            </div>
            <div className='social'>
                <a href="https://www.linkedin.com/in/mfarazahmad/">
                    <img src={"/images/linkedin_logo.webp"} alt="linkedin" />
                </a>
                <a href="https://github.com/mfarazahmad">
                    <img src={"/images/github_logo.webp"} alt="github" />
                </a>
            </div>
        </div>
    )
}

export default Navbar