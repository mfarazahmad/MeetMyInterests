/* eslint-disable @next/next/no-img-element */
import React, { useEffect, useRef } from 'react'
import Link from 'next/link'
import styles from '../styles/Home.module.css'

import Outline from '../components/Layout/Outline'

const Home = (props) => {

    // ----------------  UI State ----------------

    const canvasRef = useRef(null);

    // ---------------- UI Logic ----------------

    useEffect(() => {

        const canvas = canvasRef.current;

        var windowWidth = window.innerWidth;
        var windowHeight = window.innerHeight;

        canvas.width = windowWidth;
        canvas.height = windowHeight;

        var c = canvas.getContext('2d');

        var maxContainerSize = 100;

        // Random Generators
        const randomPos = () => {
            let x = Math.floor(Math.random() * (window.innerWidth));
            let y = Math.floor(Math.random() * (windowHeight));
            return [x, y];
        }

        const randomColor = () => {
            let red = Math.floor(Math.random() * 255);
            let blue = Math.floor(Math.random() * 255);
            let green = Math.floor(Math.random() * 255);
            return `rgba(${red}, ${green}, ${blue}, 0.3)`;
        }

        const randomSize = () => {
            let size = Math.floor(Math.random() * windowHeight / 20);
            return size;
        }

        const randomRadius = () => {
            let r = Math.floor(Math.random() * windowHeight / 20);
            return r;
        }

        const randomVelocity = () => {
            let dx = (Math.random() - .5);
            let dy = (Math.random() - .5);
            return [dx, dy];
        }

        // Shapes
        class Circle {
            constructor(color, x, y, dx, dy, r) {
                this.x = x;
                this.y = y;
                this.dx = dx;
                this.dy = dy;
                this.radius = r;
                this.minRadius = r;
                this.color = color;
            }

            draw = () => {
                // Coordinates begin at center of circle
                c.beginPath();
                c.strokeStyle = this.color;
                c.fillStyle = this.color;
                c.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
                c.stroke();
                c.fill();
            }

            update = () => {
                if (this.x + this.radius > windowWidth || this.x - this.radius < 0)
                    this.dx = -this.dx;
                if (this.y + this.radius > windowHeight || this.y - this.radius < 0)
                    this.dy = -this.dy;

                this.x += this.dx;
                this.y += this.dy;

                // Interactivity
                if (mouse.x - this.x < 50 && mouse.x - this.x > -50
                    && mouse.y - this.y < 50 && mouse.y - this.y > -50) {

                    if (this.radius < maxContainerSize) this.radius += 1;

                } else if (this.radius > this.minRadius) {
                    this.radius -= 1;
                }

                this.draw();
            }
        }

        class Rectangle {
            constructor(color, x, y, dx, dy, height, width) {
                this.x = x;
                this.y = y;
                this.dx = dx;
                this.dy = dy;
                this.height = height;
                this.width = width;
                this.minSize = width;
                this.color = color;
            }

            draw = () => {
                // Coordinates begin from top left
                c.fillStyle = this.color;
                c.fillRect(this.x, this.y, this.height, this.width);
                c.stroke();
            }

            update = () => {
                if (this.x + this.height > windowWidth || this.x < 0)
                    this.dx = -this.dx;
                if (this.y + this.height > windowHeight || this.y < 0)
                    this.dy = -this.dy;

                this.x += this.dx;
                this.y += this.dy;


                // Interactivity
                if (mouse.x - this.x < 50 && mouse.x - this.x > -50
                    && mouse.y - this.y < 50 && mouse.y - this.y > -50) {

                    if (this.height < maxContainerSize) {
                        this.height += 1;
                        this.width += 1;
                    };

                } else if (this.height > this.minSize) {
                    this.height -= 1;
                    this.width -= 1;
                }

                this.draw();
            }
        }

        class PingPong {
            constructor(color, x, y, dx, dy, r) {
                this.x = x;
                this.y = y;
                this.dx = dx;
                this.dy = dy;
                this.radius = r;
                this.minRadius = r;
                this.color = color;
            }

            draw = () => {
                c.beginPath();
                c.strokeStyle = this.color;
                c.fillStyle = this.color;
                c.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
                c.stroke();
                c.fill();
            }

            update = () => {
                if (this.x + this.radius > windowWidth || this.x - this.radius < 0)
                    this.dx = -this.dx;
                if (this.y + this.radius > windowHeight || this.y - this.radius < 0)
                    this.dy = -this.dy;

                this.x += this.dx;
                this.y += this.dy;

                // Top Left
                if ((barPos.x - this.x < 50 && barPos.x - this.x > 0) && (barPos.y - this.y < 25 && barPos.y - this.y > 0)) {
                    if (keys.y === keys.v || keys.y === -keys.v) {
                        this.dy = -this.dy;
                    } else if (keys.x === keys.v || keys.x === -keys.v) {
                        this.dx = -this.dx;
                    }

                }
                // Top Right
                else if ((barPos.x - this.x < -50 && barPos.x - this.x < 0) && (barPos.y - this.y < 25 && barPos.y - this.y > 0)) {
                    if (keys.y === keys.v || keys.y === -keys.v) {
                        this.dy = -this.dy;
                    } else if (keys.x === keys.v || keys.x === -keys.v) {
                        this.dx = -this.dx;
                    }

                }
                // Bottom Right
                else if ((barPos.x - this.x < -50 && barPos.x - this.x < 0) && (barPos.y - this.y < -25 && barPos.y - this.y < 0)) {
                    if (keys.y === keys.v || keys.y === -keys.v) {
                        this.dy = -this.dy;
                    } else if (keys.x === keys.v || keys.x === -keys.v) {
                        this.dx = -this.dx;
                    }


                }
                // Bottom Left
                else if ((barPos.x - this.x < 50 && barPos.x - this.x > 0) && (barPos.y - this.y < -25 && barPos.y - this.y < 0)) {
                    if (keys.y === keys.v || keys.y === -keys.v) {
                        this.dy = -this.dy;
                    } else if (keys.x === keys.v || keys.x === -keys.v) {
                        this.dx = -this.dx;
                    }
                }

                this.draw();
            }
        }

        class Bar {
            constructor(color, x, y, width, height) {
                this.x = x;
                this.y = y;
                this.width = width;
                this.height = height;
                this.color = color;
            }

            draw = () => {
                c.fillStyle = this.color;
                c.fillRect(this.x, this.y, this.width, this.height);
                c.stroke();
            }

            update = () => {

                if (this.x + this.width > windowWidth || this.x < 0)
                    keys.x = -keys.x;
                if (this.y + this.height > windowHeight || this.y < 0)
                    keys.y = -keys.y;

                this.x += keys.x;
                this.y += keys.y;

                barPos.x = this.x;
                barPos.y = this.y;

                this.draw();
            }
        }

        // Animation Trackers
        var mouse = {
            x: undefined,
            y: undefined
        }

        var keys = {
            x: 0,
            y: 0,
            v: 3
        }

        var barPos = {
            x: undefined,
            y: undefined,
        }

        var circles = [];
        var rectangles = [];
        var pingpong = [];

        // Canvas Creation
        const init = () => {
            circles = [];
            rectangles = [];
            pingpong = [];

            // Create Background Circles | Rectangles
            for (var i = 0; i < 300; i++) {

                let size = randomSize();
                let r = randomRadius();
                let color = randomColor();
                let [x, y] = randomPos();
                let [dx, dy] = randomVelocity()

                var circle = new Circle(color, x, y, dx, dy, r);
                circles.push(circle);

                var rectangle = new Rectangle(color, x, y, dx, dy, size, size);
                rectangles.push(rectangle);
            }

            // Create Ping Pong Game
            var pongball = new PingPong('white', windowWidth / 2, 100, 2, 2, 15);
            var bar = new Bar(`rgba(247, 255, 0, 0.8)`, windowWidth / 2, windowHeight - 200, 100, 50);

            pingpong.push(pongball);
            pingpong.push(bar);
        }

        // Core Animation
        const animate = () => {
            requestAnimationFrame(animate);
            c.clearRect(0, 0, windowWidth, windowHeight);

            for (var i = 0; i < circles.length; i++) {
                //circles[i].update();
                rectangles[i].update();
            }

            for (var i = 0; i < pingpong.length; i++) {
                pingpong[i].update();
            }
        }

        init();
        animate();

        // Event Listeners
        addEventListener('mousemove', function (event) {
            mouse.x = event.x;
            mouse.y = event.y;
        });

        addEventListener('keydown', function (event) {
            switch (event.key) {
                case 'ArrowLeft':
                    keys.x = -keys.v;
                    break;
                case 'ArrowUp':
                    keys.y = -keys.v;
                    break;
                case 'ArrowRight':
                    keys.x = keys.v;
                    break;
                case 'ArrowDown':
                    keys.y = keys.v;
                    break;
            }
        });

        addEventListener('resize', function () {

            windowWidth = window.innerWidth;
            windowHeight = window.innerHeight;

            canvas.width = windowWidth;
            canvas.height = windowHeight;

            init();
        });

    }, [])

    return (
        <Outline>
            <div className={styles.main}>
                <canvas ref={canvasRef} className={styles.pingpong} {...props} />
                <div className={styles.intro}>
                    <h1 className={styles.header}>Hello, my name is Faraz!</h1>
                    <h3 className={styles.header3}>Pleased to meet you.</h3>

                    <Link href="/projects" passHref>
                        <button className={styles.button}>Click Here to Learn More!</button>
                    </Link>
                </div>
                <div className={styles.pitch}>
                    <div className={styles.pitchLeft}>
                        <div className={styles.title}>
                            Engineer @
                        </div>
                        <div className={styles.companyLogos}>
                            <img src={"/images/tmobile_logo.webp"} alt="t-mobile" />
                            <img src={"/images/thd_logo.webp"} alt="home depot" />
                            <img src={"/images/pluto_logo.webp"} alt="pluto" />
                        </div>
                    </div>

                    <div className={styles.pitchRight}>
                        <div className={styles.title}>
                            Skills
                        </div>
                        <div className={styles.technologyLogos}>
                            <img src={"/images/go_logo.webp"} alt="golang" />
                            <img src={"/images/python_logo.webp"} alt="python" />
                            <img src={"/images/node_logo.webp"} alt="node" />
                            <img src={"/images/java_logo.webp"} alt="java" />
                            <img src={"/images/mongo_logo.webp"} alt="mongo" />
                            <img src={"/images/oracle_logo.webp"} alt="oracle" />
                            <img src={"/images/rabbitmq_logo.webp"} alt="rabbitmq" />
                            <img src={"/images/redis_logo.webp"} alt="redis" />
                            <img src={"/images/aws_logo.webp"} alt="aws" />
                            <img src={"/images/kubernetes_logo.webp"} alt="kubernetes" />
                            <img src={"/images/datadog_logo.webp"} alt="datadog" />
                        </div>
                    </div>
                </div>
                {/* <div className={styles.techStream}>
                    <img src={"/images/go_logo.webp"} />
                    <img src={"/images/python_logo.webp"} />
                    <img src={"/images/node_logo.webp"} />
                    <img src={"/images/java_logo.webp"} />
                    <img src={"/images/mongo_logo.webp"} />
                    <img src={"/images/oracle_logo.webp"} />
                    <img src={"/images/rabbitmq_logo.webp"} />
                    <img src={"/images/redis_logo.webp"} />
                    <img src={"/images/aws_logo.webp"} />
                    <img src={"/images/kubernetes_logo.webp"} />
                    <img src={"/images/datadog_logo.webp"} />
                </div> */}
            </div>
        </Outline>

    )
}

export default Home;