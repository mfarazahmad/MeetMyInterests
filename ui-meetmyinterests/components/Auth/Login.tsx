/* eslint-disable @next/next/no-img-element */
import React, { MouseEventHandler, useState } from 'react'

import { Form, Input, Button } from 'antd';

type Props = {
    handleLogin: MouseEventHandler<HTMLElement>,
    handleLoginDisplay: MouseEventHandler<HTMLElement>,
}

const Login = (props: Props) => {

    return (
        <div className='loginSurrounding'>
            <div className='loginBox'>
                <div className='topRow'>
                    <div className='closeBtn' onClick={props.handleLoginDisplay}>x</div>
                </div>
                <Form onFinish={props.handleLogin} className='loginForm'>
                    <Form.Item label="Username" name="username">
                        <Input />
                    </Form.Item>

                    <Form.Item label="Password" name="password">
                        <Input />
                    </Form.Item>

                    <Button className='loginBtn' htmlType="submit">Login</Button>
                </ Form>
            </div>
        </div >
    )

}

export default Login