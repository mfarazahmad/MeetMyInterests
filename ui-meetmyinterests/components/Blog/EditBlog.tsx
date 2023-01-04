import React, { useState } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'
import { EditorState } from 'draft-js'
import { stateFromHTML } from 'draft-js-import-html'
import { stateToHTML } from "draft-js-export-html";
import { Button } from 'antd';

import BlogEditor from './Editor'
import { PostDetails } from '../../types/blog'
import { editBlogByID } from '../../service/blog'

type Props = {
    setBlogActionStatus: Function,
    setAlertVisiblity: Function,
    postDetails: PostDetails,
    blogId: string,
    post: string
}

// PUT /api/v1/post/[postID]
const EditBlog = (props: Props) => {

    const router = useRouter()

    const [post, setPost] = useState<EditorState>(EditorState.createWithContent(stateFromHTML(props.post)))

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
                let data = await editBlogByID(props.blogId, payload)
                if (data.err) {
                    console.log(data.err)
                    props.setBlogActionStatus(false)
                } else {
                    console.log(data.msg)
                    props.setAlertVisiblity(true)
                    props.setBlogActionStatus(true)
                    setTimeout(() => router.reload(), 180)
                }

            } else {
                console.log('Failed to validate. Please fix errors.')
                props.setBlogActionStatus(false)
            }

        } catch (error) {
            console.log(error)
            props.setBlogActionStatus(false)
        }
    }

    return (
        <div className='editBlog'>
            <BlogEditor
                handleEditor={handleEditor}
                post={post}
            />
            <Button
                onClick={handleSubmit}
            >
                Submit
            </Button>
        </div>
    )
}

export default EditBlog