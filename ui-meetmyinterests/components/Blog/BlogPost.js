import React, { useState, useEffect } from 'react';
import axios from 'axios'

import { Button } from 'antd';

import PostCard from './PostCard'
import EditBlog from './EditBlog'

// GET /api/v1/post/[postID]
const BlogPost = (props) => {

    const getPostDetails = async (postID) => {
        try {
            let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post`
            let resp = await axios.get(`${endpoint}/${postID}`)
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
            } else {
                console.log(data.msg)
                let updatedDetails = { ...postDetails, ...data.post }
                setPostDetails(updatedDetails)
            }

        } catch (error) {
            console.log(error)
        }
    }


    useEffect(() => {
        console.log(`Retreiving Post ${props.blogId} Details`)
        getPostDetails(props.blogId)
    })

    const [postDetails, setPostDetails] = useState({})
    const [isEditMode, setEditMode] = useState(false)

    const handleEditMode = () => { setEditMode(true) }

    return (
        <div className='blogFullPage'>
            <PostCard postDetails={postDetails} />
            <div>{postDetails.subTitle}</div>

            {isEditMode && <EditBlog blogId={postDetails.blogId} />}

            {!isEditMode && (
                <div>
                    <Button onClick={handleEditMode}>Edit</Button>
                    <div dangerouslySetInnerHTML={{ __html: postDetails.post }} />
                </div>
            )}
        </div>
    )
}

export default BlogPost;