import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'
import { EditorState } from 'draft-js'
import { stateFromHTML } from 'draft-js-import-html'
import { stateToHTML } from "draft-js-export-html";
import { Button } from 'antd';

import BlogEditor from './Editor'

// PUT /api/v1/post/[postID]
const EditBlog = (props) => {

    const router = useRouter()

    const [post, setPost] = useState(EditorState.createWithContent(stateFromHTML(props.post)))

    const handleEditor = (e) => {
        console.log(e);
        setPost(e);
    }

    //TODO 
    const validateBlog = (payload) => {

        return true
    }

    const handleSubmit = async () => {

        try {
            let htmlPost = stateToHTML(post.getCurrentContent())
            let payload = props.postDetails;
            payload.post = htmlPost;
            console.log(payload)
            let isValid = validateBlog(payload)

            if (isValid) {
                let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post`
                let resp = await axios.put(`${endpoint}/${props.blogId}`, JSON.stringify(payload))
                let data = resp.data;

                if (data.err) {
                    console.log(data.err)
                } else {
                    console.log(data.msg)
                    alert(data.msg)
                    router.reload()
                }

            } else {
                console.log('Failed to validate. Please fix errors.')
            }

        } catch (error) {
            console.log(error)
        }

    }

    return (
        <div className='editBlog'>
            <BlogEditor handleEditor={handleEditor} post={post} />

            <Button
                onClick={handleSubmit}
            >
                Submit</Button>
        </div>
    )
}

export default EditBlog