/* eslint-disable @next/next/no-img-element */
import React, { MouseEventHandler, useState } from 'react'

import { Form, Input, Button } from 'antd';
import { oauthUserLogin } from '../../service/auth';

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
                    <Button 
                        style={{"marginTop":"10px"}} 
                        icon={ <img style={{"height": "20px", "marginRight": "10px"}} 
                            src={"/images/google-auth.svg"} alt="Google Logo" />}
                        onClick={() => oauthUserLogin() }
                    >
                        Login with Google
                    </Button>
                </ Form>
            </div>
        </div >
    )

}

export default Login