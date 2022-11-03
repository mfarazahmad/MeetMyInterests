import React from 'react';
import { PostDetails } from '../../types/blog';
import { Tag } from 'antd';


type Props = {
    blogId: string,
    handleFullPage: Function,
    postDetails: PostDetails
}

const PostCard = (props: Props) => {

    return (
        <div className='postCard' onClick={() => props.handleFullPage(props.blogId)} >
            <div className='postTopRow'>
                <h4 className='postDate'>{props.postDetails.date}</h4>
                <div>|</div>
                <Tag color="red">{props.postDetails.category}</Tag>
            </div>
            <h1 className='postTitle'>{props.postDetails.title}</h1>
        </div>
    )
}

export default PostCard;