/* eslint-disable @next/next/no-img-element */
import React, { useState, useEffect } from 'react'
import axios from 'axios'

import { Tag } from 'antd';

const ProjectShowCase = () => {

    useEffect(() => {

    })


    return (
        <div className='projectShowCase'>
            <a href='https://github.com/mfarazahmad/MeetMyInterests'>
                <div className='project'>
                    <div className='projectText'>
                        <h4 className="projectTitle">MeetMyInterests</h4>
                        <p className="projectDesc">A Scalable Web App Built with Micro Services that represent my brand. Showcases Blog Tutorials, Professional Experiences, and Hobbies.</p>
                        <div className='projectTagBox'>
                            <Tag color="red">Golang</Tag>
                            <Tag color="yellow">React</Tag>
                            <Tag color="green">RabbitMQ</Tag>
                            <Tag color="purple">GRPC</Tag>
                            <Tag color="blue">Mongo</Tag>
                        </div>
                    </div>
                    <img className="projectImg" src={"/images/meetmyinterests.webp"} alt="meetmyinterests" meta="golang, react, mongo, rabbitmq, grpc" />
                </div>
            </a>
            <a href='https://github.com/mfarazahmad/CabbageSoup.co'>
                <div className='project'>
                    <img className="projectImg" src={"/images/cabbagesoup.co.webp"} alt="cabbagesoup.co" meta="python, node, react, mongo" />
                    <div className='projectText'>
                        <h4 className="projectTitle">CabbageSoup.co</h4>
                        <p className="projectDesc">The marketing portal and demo site for cabbagesoup.co, a Software Engineering firm based out of Atlanta,GA.</p>
                        <div className='projectTagBox'>
                            <Tag color="red">Node</Tag>
                            <Tag color="yellow">React</Tag>
                            <Tag color="yellow">Next.js</Tag>
                            <Tag color="purple">Python</Tag>
                            <Tag color="blue">Mongo</Tag>
                        </div>
                    </div>
                </div>
            </a>
            <a href='https://github.com/mfarazahmad/service-photo-management'>
                <div className='project'>
                    <div className='projectText'>
                        <h4 className="projectTitle">Service-Photo-Management</h4>
                        <p className="projectDesc">A service created to manage my photography in google cloud. </p>
                        <div className='projectTagBox'>
                            <Tag color="red">Golang</Tag>
                        </div>
                    </div>
                    <img className="projectImg" src={"/images/service-photo-management.webp"} alt="service-photo-management" meta="golang" />
                </div>
            </a>
        </div >
    )

}

export default ProjectShowCase