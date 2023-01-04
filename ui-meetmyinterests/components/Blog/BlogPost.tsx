import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router'
import axios from 'axios'
import { PostDetails } from '../../types/blog';

import { Button } from 'antd';

import PostCard from './PostCard'
import EditBlog from './EditBlog'
import { LoginContext } from '../../context/ctx';
import CustomAlert from '../Widgets/Alert';
import { deleteBlogByID, getBlogByID } from '../../service/blog';

type Props = {
    blogId: string,
    handleFullPage: Function,
}
// GET /api/v1/post/[postID]
const BlogPost = (props: Props) => {

    const getPostDetails = async (postID: string) => {
        try {
            let data = await getBlogByID(postID)
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

    const [postDetails, setPostDetails] = useState<PostDetails>({ blogId: "", subTitle: "", post: "", category: "", date: "", title: "", })
    const [isEditMode, setEditMode] = useState(false)
    const [alertVisible, setAlertVisiblity] = useState<boolean>(false)
    const [isblogActionComplete, setBlogActionStatus] = useState<boolean>(false)

    const router = useRouter()

    const handleEditMode = () => { setEditMode(true) }

    const handleDeleteMode = async () => {
        try {
            let data = await deleteBlogByID(postDetails.blogId);
            if (data.err) {
                console.log(data.err)
                setBlogActionStatus(false)
            } else {
                console.log(data.msg)
                setAlertVisiblity(true)
                setBlogActionStatus(true)
                setTimeout(() => router.reload(), 180)
            }

        } catch (error) {
            console.log(error)
            setBlogActionStatus(false)
        }
    }

    const handleBackBtn = () => {
        router.reload()
    }

    return (
        <div className='blogFullPage'>

            <CustomAlert
                alertVisible={alertVisible}
                successCheck={isblogActionComplete}
                setAlertVisiblity={setAlertVisiblity}
                successMsg='Successfully modified post!'
                failedMsg="Failed to modify post"
            />

            <PostCard handleFullPage={props.handleFullPage} postDetails={postDetails} blogId={postDetails.blogId} />
            <div className='blogSubTitle'>{postDetails.subTitle}</div>

            {isEditMode && <EditBlog
                postDetails={postDetails}
                post={postDetails.post}
                blogId={postDetails.blogId}
                setAlertVisiblity={setAlertVisiblity}
                setBlogActionStatus={setBlogActionStatus}
            />}

            {!isEditMode && (
                <div className='blogEditContainer'>
                    <div className='blogEditContainerTopRow'>
                        <Button onClick={handleBackBtn}>Back</Button>
                        <LoginContext.Consumer >
                            {value =>
                                <div>
                                    {value.isLoggedIn && (
                                        <div>
                                            <Button
                                                className='blogEditBtn'
                                                onClick={handleEditMode}>Edit
                                            </Button>
                                            <Button
                                                className='blogEditBtn blogDeleteBtn'
                                                onClick={handleDeleteMode}>Delete
                                            </Button>
                                        </div>
                                    )}
                                </div>
                            }
                        </LoginContext.Consumer>
                    </div>
                    <div className='blogContent' dangerouslySetInnerHTML={{ __html: postDetails.post }} />
                </div>
            )}
        </div>
    )
}

export default BlogPost;