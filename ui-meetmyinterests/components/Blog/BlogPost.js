import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router'
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
                console.log(data.posts)
                let updatedDetails = { ...postDetails, ...data.posts[0] }
                setPostDetails(updatedDetails)
            }

        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        console.log(`Retreiving Post ${props.blogId} Details`)
        getPostDetails(props.blogId)
    }, [])

    const [postDetails, setPostDetails] = useState({})
    const [isEditMode, setEditMode] = useState(false)

    const router = useRouter()

    const handleEditMode = () => { setEditMode(true) }

    const handleDeleteMode = async () => {
        try {
            let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post`
            let resp = await axios.delete(`${endpoint}/${postDetails.blogId}`)
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
            } else {
                console.log(data.msg)
                router.reload()
            }

        } catch (error) {
            console.log(error)
        }
    }

    return (
        <div className='blogFullPage'>
            <PostCard handleFullPage={props.handleFullPage} postDetails={postDetails} blogId={postDetails.blogId} />
            <div className='blogSubTitle'>{postDetails.subTitle}</div>

            {isEditMode && <EditBlog postDetails={postDetails} post={postDetails.post} blogId={postDetails.blogId} />}

            {!isEditMode && (
                <div className='blogEditContainer'>
                    <div className='blogEditContainerTopRow'>
                        <Button className='blogEditBtn' onClick={handleEditMode}>Edit</Button>
                        <Button className='blogEditBtn blogDeleteBtn' onClick={handleDeleteMode}>Delete</Button>
                    </div>
                    <div className='blogContent' dangerouslySetInnerHTML={{ __html: postDetails.post }} />
                </div>
            )}
        </div>
    )
}

export default BlogPost;