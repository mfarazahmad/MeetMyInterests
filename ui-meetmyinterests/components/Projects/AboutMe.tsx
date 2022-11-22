/* eslint-disable @next/next/no-img-element */
import React from 'react'

const AboutMe = () => {

    return (
        <div className='aboutMe'>
            <img className="profileImg" src={"/images/profile.webp"} alt="faraz" />
            <div className='aboutMeText'>
                My name is Faraz! I am a Sr. Software Engineer with over 5 years of experience developing Enterprise Level Scalable Microservices.
                <br /><br />
                I often work on implementing technologies like REST APIs, GRPC, Message Queues, Cacheing, Cloud Infrastructure, Monitoring as well as a variety of SQL/ NO-SQL Databases.
                <br /><br />
                I teach Software Engineering for free to limited class sizes on the side, love to sing, film, and photograph the world around me.
            </div>
        </div >
    )

}

export default AboutMe