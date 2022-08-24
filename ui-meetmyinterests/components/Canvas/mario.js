import React, {useEffect, createRef, useRef, useState} from 'react'
import marioImg from '../public/mario.png'

const Mario = (props) => {

    // ----------------  UI State ----------------

    const ref = createRef(null);

    // ---------------- UI Logic ----------------

    useEffect(() => {

        const canvas = ref.current

        var windowWidth = window.innerWidth
        var windowHeight = window.innerHeight

        canvas.width = windowWidth
        canvas.height = windowHeight

        const c = canvas.getContext('2d')

        const gravity = .5
        let scrollOffset = 0

        var platforms = []
        var character;

        const charImg = new Image()
        charImg.src = marioImg.src


        const oldMovementLogic = (position) => {
            if (position.x + 50 > windowWidth) {
                position.x -= 50;
            } else if (position.y + 50 > windowHeight) {
                //this.position.y -= 50;
            } else if (position.y < 0) {
                position.y += 50;
            } else if (position.x < 0) {
                position.x += 50;
            }

            if (keys.x === -keys.v) {
                position.x -= 50;
                keys.x = 0;
            } else if (keys.x === keys.v) {
                position.x += 50;
                keys.x = 0;
            }

            if (keys.y === -keys.v) {
                position.y -= 50;
                keys.y = 0;
            } else if (keys.y === keys.v ) {
                position.y += 50;
                keys.y = 0;
            }
        }

        // Shapes
        class Platform {
            constructor(x, y, height, width, color) {
                this.x = x
                this.y = y
                this.velocity = {x: .1, y: 0}
                this.height = height
                this. width = width
                this.color = color
            }

            draw = () => {
                c.fillStyle = this.color
                c.fillRect(this.x, this.y, this.width, this.height)
                c.shadowBlur = 20
                c.shadowColor = "black"
                c.stroke()
            }

            update = () => {

                this.x += this.velocity.x

                if (this.x + this.width > windowWidth ) {
                    this.velocity.x = -this.velocity.x
                } else if (this.x + this.width < windowWidth*5/12 ) {
                    this.velocity.x = -this.velocity.x
                }

                this.draw();
            }
        }

        class Character {
            constructor(x, y, image) {
                this.position = {x, y}
                this.velocity = {x: 0, y: 0}
                this.image = image
                this.height = 50
                this. width = 50
            }

            draw = () => {
                c.drawImage(this.image, this.position.x, this.position.y, this.height, this. width)

                // c.fillStyle = 'green';
                // c.fillRect(this.position.x, this.position.y, 50, 50);
                // c.stroke();
                
            }

            update = () => {
                this.position.x += this.velocity.x
                this.position.y += this.velocity.y

                // Gravity
                if (this.position.y + this.height + this.velocity.y <= windowHeight) {
                    this.velocity.y += gravity
                } else this.velocity.y = 0

                this.draw()
            }
        }

        // Animation Trackers
        var keys = {
            right: {pressed: false},
            left: {pressed: false}
        }

        // Canvas Creation
        const init = () => {
            var heightIncrease = 0;
            var widthSpacing = 1.5;

            // Platformer Game
            for (var i =0; i < 8; i++) {
                if (i < 5) {
                    widthSpacing += 1;
                    heightIncrease -= 50;
                } else if (i === 5) {
                    widthSpacing -= 1;
                    heightIncrease -= 150;
                } else {
                    widthSpacing -= 1;
                    heightIncrease -= 50;
                }

                var platform = new Platform(windowWidth*widthSpacing/7, windowHeight-100+heightIncrease, 15, 80, 'brown');
                platforms.push(platform);
            }

            //square_character = new Character(windowWidth/9, windowHeight/2, 40, 40, 'green');
            character = new Character(windowWidth/9, windowHeight/2, charImg);
        }



        // Core Animation
        const animate = () => {
            requestAnimationFrame(animate);
            c.clearRect(0, 0,windowWidth, windowHeight)

            character.update()

            platforms.forEach((platform)  => {
                platform.update();
                
                // Platform Collision Detection
                if  (   character.position.y + character.height <= platform.y &&
                        character.position.y + character.height + character.velocity.y >= platform.y &&
                        character.position.x + character.width >= platform.x && 
                        character.position.x <= platform.x + platform.width
                    ) {
                    character.velocity.y = 0
                }

                // Platform Movement
                if (keys.right.pressed && character.position.x >= windowWidth*3/7) {
                    scrollOffset += 5
                    platform.x -= 2
                } else if (keys.left.pressed) {
                    scrollOffset -= 5
                    platform.x += 2
                }
            })

            // Character Movement
            if (keys.right.pressed && character.position.x < windowWidth*3/7) {
                character.velocity.x = 2
            } else if (keys.left.pressed && character.position.x > 1/7) {
                character.velocity.x = -2
            } else character.velocity.x = 0

            if (scrollOffset > 14000) {
                console.log("You Win!")
            }

        }

        init()
        animate()

        // Event Listeners
        addEventListener('keydown', ({key}) => {
            switch (key) {
                case 'ArrowLeft':
                    keys.left.pressed = true
                    break

                case 'ArrowUp':
                    character.velocity.y -= 10
                    break

                case 'ArrowRight':
                    keys.right.pressed = true
                    break

                case 'ArrowDown':
                    break
            }
        });

        addEventListener('keyup', ({key}) => {
            switch (key) {
                case 'ArrowLeft':
                    keys.left.pressed = false
                    break

                case 'ArrowUp':
                    //character.velocity.y -= 10
                    break

                case 'ArrowRight':
                    keys.right.pressed = false
                    break

                case 'ArrowDown':
                    break
            }
        });

        addEventListener('resize', () => {

            windowWidth = window.innerWidth;
            windowHeight = window.innerHeight;

            canvas.width = windowWidth;
            canvas.height = windowHeight;

            init();
        });

    }, []);

    return (

    <div className='main'>
        <canvas ref={ref} className='mario' {...props}/>
        <h1 className='title'>Testing Character Jump</h1>
    </div>

    )
}

export default Mario;