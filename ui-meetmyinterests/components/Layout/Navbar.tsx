/* eslint-disable @next/next/no-img-element */
import React, { MouseEventHandler } from 'react'
import Link from 'next/link'

import { Avatar, Badge, Button } from 'antd'

import Login from '../Auth/Login'
import Logout from '../Auth/Logout'

type Props = {
    isLoggedIn: boolean,
    showLoginBox: boolean,
    username: string,
    handleLogin: MouseEventHandler<HTMLElement>,
    handleLogout: MouseEventHandler<HTMLElement>,
    handleLoginDisplay: MouseEventHandler<HTMLElement>,
}

const Navbar = (props: Props) => {

    return (
        <div className="navbar">

            <div className='welcomeMsg'>
                <img className="brandLogo" src={"/images/Faraz-Brand-Logo.webp"} alt="brand-logo" />

                <div>
                    Welcome, <strong>{props.username}</strong>
                </div>
                <div>
                    {props.isLoggedIn &&
                        <Badge count={1}>
                            <Link href="/dashboard" passHref>
                                <Avatar style={{ backgroundColor: 'red', verticalAlign: 'middle' }} shape="square" size="large" gap={5}>
                                    Dash
                                </Avatar>
                            </Link>
                        </Badge>
                    }
                </div>
            </div>

            {props.showLoginBox && <Login handleLoginDisplay={props.handleLoginDisplay} handleLogin={props.handleLogin} />}

            {props.isLoggedIn ?
                (
                    <div>
                        <Logout handleLogout={props.handleLogout} />
                    </div>
                ) :
                (
                    <div>
                        <Button className='loginBtn' onClick={props.handleLoginDisplay}>Login</Button>
                    </div>
                )
            }

            <div className='linkTags'>
                <Link href="/"><a>Home</a></Link>
                <Link href="/projects"><a>Projects</a></Link>
                <Link href="/blog"><a>Blog</a></Link>

                {props.isLoggedIn &&
                    <Link href="/fitness"><a>Fitness</a></Link>
                }
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