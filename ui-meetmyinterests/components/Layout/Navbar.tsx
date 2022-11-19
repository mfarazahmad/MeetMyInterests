/* eslint-disable @next/next/no-img-element */
import React, { MouseEventHandler } from 'react'
import Link from 'next/link'

import { Avatar, Badge, Button } from 'antd'

import Login from '../Auth/Login'
import Logout from '../Auth/Logout'

type Props = {
    isLoggedIn: boolean,
    handleLogin: MouseEventHandler<HTMLElement>,
    handleLogout: MouseEventHandler<HTMLElement>,
    showLoginBox: boolean,
    handleLoginDisplay: MouseEventHandler<HTMLElement>,
}

const Navbar = (props: Props) => {

    return (
        <div className="navbar">
            <div className='welcomeMsg'>
                <div>
                    Welcome, Faraz
                </div>
                <div>
                    <Badge count={1}>
                        {props.isLoggedIn ? (
                            <Link href="/dash" passHref>
                                <Avatar style={{ backgroundColor: 'red', verticalAlign: 'middle' }} shape="square" size="large" gap={5}>
                                    Dash
                                </Avatar>
                            </Link>
                        ) : (
                            <Avatar style={{ backgroundColor: 'gray', verticalAlign: 'middle' }} shape="square" size="large" gap={5}>
                                Dash
                            </Avatar>
                        )
                        }
                    </Badge>
                </div>
            </div>

            {props.showLoginBox && <Login handleLoginDisplay={props.handleLoginDisplay} handleLogin={props.handleLogin} />}

            {!props.isLoggedIn ?
                (
                    <div>
                        <Button className='loginBtn' onClick={props.handleLoginDisplay}>Login</Button>
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