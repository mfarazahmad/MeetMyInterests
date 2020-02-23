const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const path = require('path')

// Allows use of environment variables
require('dotenv').config()

// Create express app
const app = express()

app.use(cors())
app.use(express.json())
app.use(express.static(path.join(__dirname, '..', 'build')))

const port = process.env.PORT | 7222;

// Serve the React Frontend
app.route('/').get((req, res) => {
    res.sendFile(path.join(__dirname, '..', 'build', 'index.html'))
})

// Connect to Database
const dbURL = process.env.MONGO_URL
mongoose.connect(dbURL, {useUnifiedTopology: true, useNewUrlParser: true, useCreateIndex: true})
mongoose.connection.on('error', () => console.log('An error occurred from the database'))
mongoose.connection.once('open', () => console.log('Succesfully connected to the database'))

// Configure App Routes
const homeRouter = require('./routes/homeRouter')
const contactRoute = require('./routes/contactRouter')
const dashboardRoute = require('./routes/dashboardRouter')

app.use('/home', homeRouter)
app.use('/contact', contactRoute)
app.use('/dashboard', dashboardRoute)

// Start Node server
app.listen(port, () => {
    console.log(`Listening on port: ${port}`)
})