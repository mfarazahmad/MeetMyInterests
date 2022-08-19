import React, {useState, useEffect} from 'react';
import Link from 'next/link'

import {Avatar, Badge} from 'antd';

const Navbar = () => {

    return (
        <div className="navbar">
             <div className='welcomeMsg'>
                <div>
                Welcome, Faraz
                </div>
                <div>
                    <Badge count={1}>
                    <Link href="/dash">
                        <Avatar style={{ backgroundColor: 'red', verticalAlign: 'middle' }}  shape="square" size="large" gap={5}>
                            Dash
                        </Avatar>
                    </Link>
                    </Badge>
                </div>
            </div>
            <div className='linkTags'>
                <Link href="/"><a>Home</a></Link>
                <Link href="/projects"><a>Projects</a></Link>
                <Link href="/blog"><a>Blog</a></Link>
                <Link href="/fitness"><a>Fitness</a></Link>
            </div>
        </div>
    )
}

export default Navbar;