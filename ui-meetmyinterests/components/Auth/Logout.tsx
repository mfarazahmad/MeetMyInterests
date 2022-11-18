/* eslint-disable @next/next/no-img-element */
import React, { MouseEventHandler } from 'react'

import { Button } from 'antd';

type Props = {
    handleLogout: MouseEventHandler<HTMLElement>,
}

const Logout = (props) => {

    return (
        <div className='logoutBox'>
            <Button className='loginBtn' onClick={props.handleLogout}>Logout</Button>
        </div >
    )

}

export default Logout