import React, { useState, useEffect } from 'react'
import axios from 'axios'

import styles from '../styles/Blog.module.css'
import Outline from '../components/Layout/Outline'
import NewBlogPost from '../components/Blog/NewBlogPost'
import BlogPost from '../components/Blog/BlogPost'
import PostCard from '../components/Blog/PostCard'

// GET /api/v1/post
const Blog = () => {

    const [posts, setPosts] = useState([])
    const [viewNewBlog, setViewNewBlog] = useState(false)
    const [viewBlogFullPage, setBlogFullPage] = useState(false)
    const [currentBlogID, setBlogId] = useState(0)

    const getPosts = async () => {
        try {
            let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post/5` //?limit=5
            let resp = await axios.get(`${endpoint}`)
            let data = resp.data;
            console.log(data)

            if (data.err) {
                console.log(data.err)
            } else {
                console.log(data.msg)

                console.log([...posts, ...data.posts])
                setPosts(posts => [...posts, ...data.posts])
            }

        } catch (error) {
            console.log(error)
        }
    }


    useEffect(() => {
        console.log('Retrieving the latest Posts')
        getPosts()
    }, [])

    const handleNewBlogView = () => setViewNewBlog(viewNewBlog => !viewNewBlog)

    const handleFullPage = blogId => {
        setBlogId(blogId)
        setBlogFullPage(true)
    }

    return (
        <Outline>
            <div className={styles.main}>
                <h1 className={styles.header}>BLOG</h1>
                <button
                    className={styles.newPostBtn}
                    onClick={handleNewBlogView}
                >+</button>

                {viewNewBlog && (
                    <NewBlogPost handleNewBlogView={handleNewBlogView} />
                )}

                {viewBlogFullPage && <BlogPost blogId={currentBlogID} />}

                {!viewBlogFullPage && posts && posts.map((post, i) => {
                    return (
                        <PostCard key={i} blogId={post.blogId} handleFullPage={handleFullPage} postDetails={post} />
                    )
                })}
            </div>
        </Outline>
    )
}

export default Blog;