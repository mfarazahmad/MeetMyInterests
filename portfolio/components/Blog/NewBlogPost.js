import React, {useState, useEffect} from 'react';
import axios from 'axios'

import {Input, Button, Select} from 'antd';

const {TextArea} = Input

// POST /api/v1/create-post
const NewBlogPost = (props) => {

    const [title, setTitle] = useState('')
    const [subTitle, setSubtitle] = useState('')
    const [category, setCategory] = useState('')
    const [date, SetDate] = useState('')
    const [post, setPost] = useState('')

    const handleInputs = (e, inputName) => {
        let value = e.target.value;
        console.log(value, inputName)

        switch(inputName) {
            case 'title':
                setTitle(value)
                break;
            case 'subTitle':
                setSubtitle(value)
                break;
            case 'category':
                setCategory(value)
                break;
            case 'date':
                SetDate(value)
                break;
            case 'post':
                setPost(value)
                break;
        }
    }

    //TODO 
    const validateBlog = (payload) => {

        return true
    }

    const handleSubmit = async () => {

        try {
            let payload = {title, subTitle, category, date, post};
            let isValid = validateBlog(payload)

            if (isValid) {
                let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/create-post`
                let resp = await axios.post(`${endpoint}`, payload)
                let data = resp.data;
    
                if (data.err) {
                    console.log(data.err)
                } else {
                    console.log(data.msg)
                }

            } else {
                console.log('Failed to validate. Please fix errors.')
            }
            
        } catch (error) {
            console.log(error)
        }

    }

    return (
        <div className='newBlogPost'>
            <div className='topMenuBlog'>
                <Button 
                    onClick={props.handleNewBlogView}
                >
                    x
                </Button>
            </div>
            <div className='mainNewBlog'>
                <h2>New POST</h2>

                <Input 
                    value={title}
                    onChange={e => handleInputs(e, 'title')}
                    type="text" 
                    placeholder="Title" 
                />
                <Input 
                    value={subTitle}
                    onChange={e => handleInputs(e, 'subTitle')}
                    type="text" 
                    placeholder="Subtitle" 
                />
                <Input 
                    value={category}
                    onChange={e => handleInputs(e, 'category')}
                    type="text" 
                    placeholder="Category" 
                />
                <Input 
                    value={date}
                    onChange={e => handleInputs(e, 'date')}
                    type="text" 
                    placeholder="Date" 
                />
                <TextArea 
                    value={post}
                    onChange={e => handleInputs(e, 'post')}
                    type="text" 
                    placeholder="Post" 
                />

                <Button
                    onClick={handleSubmit}
                >
                    Submit</Button>
            </div>
        </div>
    )
}

export default NewBlogPost