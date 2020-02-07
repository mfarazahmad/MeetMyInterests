
const express = require('express')
const cors = require('cors')
const mongoose = require('mongoose')

require('dotenv').config()

const app = express()
const port = process.env.PORT || 5000

app.use(cors())
app.use(express.json())

// Connect to Database
const dbURL = process.env.DB_URL
const db = mongoose.connect(dbURLL, {useNewUrlParser: true})
db.on('error', () => {
    console.log('An error occurred from the database')
})
db.once('open', () => {
    console.log('Succesfully connected to the database')
})

// Configure App Routes
const loginRouter = require('./routes/login')
app.use('/auth', loginRouter)

// Start node server
app.listen(port, () => {
    console.log(`App is running on the following port: ${port}`)
})