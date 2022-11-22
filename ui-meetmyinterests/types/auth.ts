import { MouseEventHandler } from "react"


export type Auth = {
    'Username': string,
    'Password': string,
}

export type LoginCtx = {
    isLoggedIn: boolean,
    showLoginBox: boolean,
    handleLogin: MouseEventHandler<HTMLElement>,
    handleLogout: MouseEventHandler<HTMLElement>,
    handleLoginDisplay: MouseEventHandler<HTMLElement>,
}