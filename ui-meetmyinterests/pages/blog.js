import React, {useState, useEffect} from 'react'
import axios from 'axios'

import styles from '../styles/Blog.module.css'
import Outline from '../components/Layout/Outline'
import NewBlogPost from '../components/Blog/NewBlogPost'

// GET /api/v1/post
const Blog = () => {

    const getPosts = async () =>  {
        try {
            let endpoint = `${process.env.NEXT_PUBLIC_HOSTNAME}/api/v1/post?limit=5`
            let resp = await axios.get(`${endpoint}`)
            let data = resp.data;

            if (data.err) {
                console.log(data.err)
            } else {
                console.log(data.msg)
                let updatedPosts = posts

                data.posts.map(post => {
                    updatedPosts.push(post)
                })

                setPosts(updatedPosts)
            }
            
        } catch (error) {
            console.log(error)
        }
    }


    useEffect(() => {
        console.log('Retrieving the latest Posts')
        getPosts()
    })

    const [posts, setPosts] = useState([])
    const [viewNewBlog, setViewNewBlog] = useState(false)

    const handleNewBlogView = () => setViewNewBlog(viewNewBlog => !viewNewBlog)

    return (
        <Outline>
            <div className={styles.main}>
                <h1>BLOG</h1>
                <button
                    onClick={handleNewBlogView}
                >+</button>

                {viewNewBlog && (
                    <NewBlogPost handleNewBlogView={handleNewBlogView} />
                )}

                {posts && posts.map((post, i) => {
                    return (
                        <div 
                            className='postCard'
                            key={i}
                        >
                            <h1>{post.Title}</h1>
                            <h2>{post.Subtitle}</h2>
                            <h4>{post.Category}</h4>
                            <h4>{post.Date}</h4>
                        </div>
                    )
                })}
            </div>
        </Outline>
    )
}

export default Blog;