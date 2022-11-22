import React, { createContext } from 'react'

import { LoginCtx } from '../types/auth'

export const LoginContext = createContext<LoginCtx>(
    {
        isLoggedIn: false,
        showLoginBox: false,
        username: "User",
        handleLogin: () => null,
        handleLogout: () => null,
        handleLoginDisplay: () => null,
    }
);