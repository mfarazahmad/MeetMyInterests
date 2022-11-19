import React, { createContext, MouseEventHandler } from 'react'

type LoginContext = {
    isLoggedIn: boolean,
    showLoginBox: boolean,
    handleLogin: MouseEventHandler<HTMLElement>,
    handleLogout: MouseEventHandler<HTMLElement>,
    handleLoginDisplay: MouseEventHandler<HTMLElement>,
}

export const LoginContext = createContext<LoginContext>(
    {
        isLoggedIn: false,
        showLoginBox: false,
        handleLogin: () => null,
        handleLogout: () => null,
        handleLoginDisplay: () => null,
    }
);