import axios from "axios"
import { Auth } from "../types/auth";

export const login = async (payload: Auth) => {
    let endpoint: string = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/login`
    let resp = await axios.post(`${endpoint}`, JSON.stringify(payload))
    let data = resp.data;

    const cookieHeaders = resp.headers['Set-Cookie'];
    console.log(cookieHeaders);
    
    return data
}

export const oauthUserLogin = async () => {
    const endpoint: string | Location = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/oauth`;
    (<any> window).location = endpoint;
}

export const oauthCallBack = async (payload: any) => {
    const endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/oauth/callback`;
    let resp = await axios.post(endpoint, payload)
    let data = resp.data;
    return data
}

export const logout = async () => {
    let endpoint: string = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/user/logout`
    let resp = await axios.post(`${endpoint}`, JSON.stringify({}))
    let data = resp.data;

    window.localStorage.clear();

    return data
}