const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')

require('dotenv').config()

// Create react app
const app = express()

app.use(cors())
app.use(express.json())

PORT = process.env.PORT || 5000

// Connect to the Database
DB_URL = process.env.MONGO_URL
mongoose.connect(DB_URL, {useUnifiedTopology: true, useNewUrlParser: true, useCreateIndex: true})
mongoose.connection.on('error', () => {console.log('Error in connecting to DB')})
mongoose.connection.once('open', () => {console.log('Succesfully  connectd to database')})

const contactRoutes = require('./routes/contactRoute')
app.use('/contact', contactRoutes)

// Start node server
app.listen(PORT, () => console.log(`Liatening on port ${PORT}`))