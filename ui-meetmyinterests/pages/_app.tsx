import '../styles/globals.css'

import { useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'
import { Alert } from 'antd'

import { LoginContext } from '../context/ctx'

function MyApp({ Component, pageProps }) {

    const router = useRouter()

    const [isLoggedIn, setLoginStatus] = useState<boolean>(false)
    const [alertVisible, setAlertVisiblity] = useState<boolean>(false);
    const [showLoginBox, setLoginDisplay] = useState<boolean>(false)

    type Auth = {
        'Username': string,
        'Password': string,
    }

    const handleLogin = async (values: object) => {

        try {
            let payload: Auth = { 'Username': values['username'], 'Password': values['password'] }
            let endpoint: string = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/login`
            let resp = await axios.post(`${endpoint}`, JSON.stringify(payload))
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
                alert('Failed to login!')
            } else {
                console.log(data.msg)
                //router.push('/blog')
                //router.reload()
                setAlertVisiblity(true)
                handleLoginDisplay()
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

    const handleAlertClose = () => {
        setAlertVisiblity(alertVisible => !alertVisible);
    };

    const handleLoginDisplay = () => {
        setLoginDisplay((showLoginBox) => !showLoginBox)
    }

    return (
        <LoginContext.Provider value={{ isLoggedIn, showLoginBox, handleLogin, handleLogout, handleLoginDisplay }}>
            {alertVisible && (
                isLoggedIn ?
                    <Alert
                        message="Sucessfully logged in"
                        type="success"
                        closable
                        afterClose={handleAlertClose}
                    /> :
                    <Alert
                        message="Failed to login"
                        type="error"
                        closable
                        afterClose={handleAlertClose}
                    />
            )
            }
            <Component {...pageProps} />
        </LoginContext.Provider>
    )
}

export default MyApp
