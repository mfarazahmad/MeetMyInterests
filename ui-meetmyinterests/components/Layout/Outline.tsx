import React, { useState } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'

import Navbar from './Navbar'

type Props = {
    children: JSX.Element
}

const Outline = (props: Props) => {

    const router = useRouter()

    const [isLoggedIn, setLoginStatus] = useState(false)

    type auth = {
        'Username': string,
        'Password': string,
    }

    const handleLogin = async (values: object) => {

        try {
            let payload: auth = { 'Username': values['username'], 'Password': values['password'] }
            let endpoint: string = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/login`
            let resp = await axios.post(`${endpoint}`, JSON.stringify(payload))
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
                alert('Failed to login!')
            } else {
                console.log(data.msg)
                alert(data.msg)
                router.push('/blog')
                setLoginStatus(true)
            }

        } catch (error) {
            console.log(error)
            alert('Failed to login!')
        }
    }

    const handleLogout = async () => {
        try {
            let endpoint: string = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/logout`
            let resp = await axios.post(`${endpoint}`, JSON.stringify({}))
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
                alert('Failed to logout!')
            } else {
                console.log(data.msg)
                alert(data.msg)
                router.push('/')
                setLoginStatus(false)
            }

        } catch (error) {
            console.log(error)
            alert('Failed to logout!')
        }
    }

    return (
        <div className="outline">
            <Navbar isLoggedIn={isLoggedIn} handleLogin={handleLogin} handleLogout={handleLogout} />
            {React.cloneElement(props.children, { isLoggedIn: isLoggedIn })}
        </div>
    )
}

export default Outline;