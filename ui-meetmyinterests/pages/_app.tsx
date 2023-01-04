import '../styles/globals.css'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

import { LoginContext } from '../context/ctx'
import CustomAlert from '../components/Widgets/Alert'
import { Auth } from '../types/auth'
import { useLocalStorage } from '../utils/customHooks'
import { login, logout, oauthCallBack } from '../service/auth'

function MyApp({ Component, pageProps }) {

    const router = useRouter()

    const [isLoggedIn, setLoginStatus] = useLocalStorage<boolean>("isLoggedIn", false)
    const [alertVisible, setAlertVisiblity] = useLocalStorage<boolean>("alertVisible", false);
    const [showLoginBox, setLoginDisplay] = useLocalStorage<boolean>("showLoginBox", false)
    const [username, setUsername] = useLocalStorage<string>("username", "User")

    useEffect(() => {
        axios.defaults.withCredentials = true
        authFlow()
    }, [])

    const authFlow = async() => {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('code')) {
            let authPayload = {
                'code': urlParams.get('code'),
                'state': urlParams.get('state'),
                'scope': urlParams.get('scope')
            }

            let data:any = await oauthCallBack(authPayload);

            if (data.err) {
                setAlertVisiblity(true)
            } else {
                console.log("User is logged in!");

                setUsername("Faraz")
                setAlertVisiblity(true)
                handleLoginDisplay()
                setLoginStatus(true)

				router.push('/blog')
            }
        }
    }

    const handleLogin = async (values: object) => {

        try {
            let payload: Auth = { 'Username': values['username'], 'Password': values['password'] }
            let data = await login(payload);
            if (data.err) {
                console.log(data.err)
                setAlertVisiblity(true)
            } else {
                console.log(data.msg)
                //router.push('/blog')
                //router.reload()

                setUsername(values['username'])
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
            let data = await logout();
            if (data.err) {
                console.log(data.err)
                alert('Failed to logout!')
            } else {
                console.log(data.msg)
                alert(data.msg)
                setUsername("User")
                setLoginStatus(false)
                router.push('/')
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
        <LoginContext.Provider value={{ isLoggedIn, showLoginBox, username, handleLogin, handleLogout, handleLoginDisplay }}>
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
