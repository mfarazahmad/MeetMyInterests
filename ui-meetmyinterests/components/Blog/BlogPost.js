import React, {useState, useEffect} from 'react';
import axios from 'axios'

// GET /api/v1/post/[postID]
const BlogPost = (props) => {

    const getPostDetails = async (postID) =>  {
        try {
            let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post/`
            let resp = await axios.get(`${endpoint}/${postID}`)
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
            } else {
                console.log(data.msg)
                let updatedDetails = {...postDetails, ...data.post}
                setPostDetails(updatedDetails)
            }
            
        } catch (error) {
            console.log(error)
        }
    }


    useEffect(() => {
        console.log(`Retreiving Post ${props.postID} Details`)
        getPostDetails(props.postID)
    })

    const [postDetails, setPostDetails] = useState({})

    return (
        <div>
            <div className='postCard'>
                <h1>{postDetails.Title}</h1>
                <h2>{postDetails.Subtitle}</h2>
                <h4>{postDetails.Category}</h4>
                <h4>{postDetails.Date}</h4>
            </div>

            <div>{postDetails.Post}</div>
        </div>
    )
}

export default BlogPost;