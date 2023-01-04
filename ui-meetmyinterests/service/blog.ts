import axios from "axios"

export const getBlogs = async () => {
    let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post?limit=5`
    let resp = await axios.get(`${endpoint}`)
    let data = resp.data;
    return data
}

export const getBlogByID = async (postID: string) => {
    let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post`
    let resp = await axios.get(`${endpoint}/${postID}`)
    let data = resp.data
    return data;
}

export const newPost = async (payload: any) => {
    let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post/new`
    let resp = await axios.post(`${endpoint}`, JSON.stringify(payload))
    let data = resp.data;
    return data;
}

export const editBlogByID = async (postID: string, payload: any) => {
    let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post`
    let resp = await axios.put(`${endpoint}/${postID}`, JSON.stringify(payload))
    let data = resp.data;
    return data;
}

export const deleteBlogByID = async (postID: string) => {
    let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post`
    let resp = await axios.delete(`${endpoint}/${postID}`)
    let data = resp.data;
    return data;
}