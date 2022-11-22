import '../styles/globals.css'

import { useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

import { LoginContext } from '../context/ctx'
import CustomAlert from '../components/Widgets/Alert'

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

        axios.defaults.withCredentials = true

        try {
            let payload: Auth = { 'Username': values['username'], 'Password': values['password'] }
            let endpoint: string = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/login`
            let resp = await axios.post(`${endpoint}`,
                JSON.stringify(payload))
            let data = resp.data;
            const cookieHeaders = resp.headers['Set-Cookie'];
            console.log(cookieHeaders);

            if (data.err) {
                console.log(data.err)
                setAlertVisiblity(true)
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
            setAlertVisiblity(true)
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

    const handleLoginDisplay = () => {
        setLoginDisplay((showLoginBox) => !showLoginBox)
    }

    return (
        <LoginContext.Provider value={{ isLoggedIn, showLoginBox, handleLogin, handleLogout, handleLoginDisplay }}>
            <CustomAlert
                alertVisible={alertVisible}
                successCheck={isLoggedIn}
                setAlertVisiblity={setAlertVisiblity}
                successMsg="Sucessfully logged in"
                failedMsg="Failed to login"

            />
            <Component {...pageProps} />
        </LoginContext.Provider>
    )
}

export default MyApp
