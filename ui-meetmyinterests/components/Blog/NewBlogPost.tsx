import React, { useState, MouseEventHandler } from 'react';
import { useRouter } from 'next/router'
import axios from 'axios'
import { stateToHTML } from "draft-js-export-html";
import { EditorState } from 'draft-js';

import { Alert, Input, Button, Select, AlertProps } from 'antd';

import BlogEditor from './Editor'
import CustomAlert from '../Widgets/Alert';

const { Option } = Select;

type Props = {
    handleNewBlogView: MouseEventHandler<HTMLElement>,
}

type PostMessage = {
    msg: string,
    type: AlertProps["type"]
}

// POST /api/v1/post/new
const NewBlogPost = (props: Props) => {

    const router = useRouter()

    const [title, setTitle] = useState<string>('')
    const [subTitle, setSubtitle] = useState<string>('')
    const [category, setCategory] = useState<string>('')
    const [post, setPost] = useState<EditorState>('')
    const [alertVisible, setAlertVisiblity] = useState<boolean>(false);
    const [isPostSaved, setPostStatus] = useState<boolean>(false)

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

        let newPostMsg: PostMessage;

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
                    setPostStatus(false)
                } else {
                    console.log(data.msg)
                    setPostStatus(true)
                }

            } else {
                console.log('Failed to validate.')
                setPostStatus(false)
            }

        } catch (error) {
            console.log(error)
            setPostStatus(false)
        }

        setAlertVisiblity(true)
        setTimeout(() => router.reload(), 180)
    }

    return (
        <div className='popOutContainer'>

            <CustomAlert
                alertVisible={alertVisible}
                successCheck={isPostSaved}
                setAlertVisiblity={setAlertVisiblity}
                successMsg='Successfully added post!'
                failedMsg='Failed to post article!'
            />

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