import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router'
import axios from 'axios'
import { stateToHTML } from "draft-js-export-html";

import { Input, Button, Select } from 'antd';

import BlogEditor from './Editor'

const { Option } = Select;

// POST /api/v1/post/new
const NewBlogPost = (props) => {

    const router = useRouter()

    const [title, setTitle] = useState('')
    const [subTitle, setSubtitle] = useState('')
    const [category, setCategory] = useState('')
    const [post, setPost] = useState('')

    const handleInputs = (e, inputName) => {
        let value = e.target.value;
        console.log(value, inputName)

        switch (inputName) {
            case 'title':
                setTitle(value)
                break;
            case 'subTitle':
                setSubtitle(value)
                break;
        }
    }

    const handleSelect = (value) => {
        setCategory(value)
    }

    const handleEditor = (e) => {
        console.log(e);
        setPost(e);
    }

    //TODO 
    const validateBlog = (payload) => {

        return true
    }

    const getCurrentDate = () => {
        let today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();

        return mm + '/' + dd + '/' + yyyy;
    }

    const handleSubmit = async () => {

        try {
            let htmlPost = stateToHTML(post.getCurrentContent())
            let date = getCurrentDate();

            let payload = { title, subTitle, category, date, post: htmlPost };
            console.log(payload)
            let isValid = validateBlog(payload)

            if (isValid) {
                let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post/new`
                let resp = await axios.post(`${endpoint}`, JSON.stringify(payload))
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
        <div className='popOutContainer'>
            <div className='newBlogPost'>
                <div className='topMenuBlog'>
                    <Button
                        onClick={props.handleNewBlogView}
                    >
                        x
                    </Button>
                </div>
                <div className='mainNewBlog'>
                    <h2 className='newPostTitle'>CREATE POST</h2>

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
                    <Select
                        value={category}
                        onChange={handleSelect}
                        type="text"
                        placeholder="Category"
                    >
                        <Option value="cs">CS</Option>
                        <Option value="musings">Musings</Option>
                    </Select>

                    <BlogEditor handleEditor={handleEditor} post={post} />

                    <Button
                        onClick={handleSubmit}
                    >
                        Submit</Button>
                </div>
            </div>
        </div>
    )
}

export default NewBlogPost