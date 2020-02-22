const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const dotenv = require('dotenv')
const parse_json = require('parse-json')

// Allows use of environment variables
dotenv.config()

const app = express()

app.use(cors())
app.use(express.json())

const port = 7222;

// Connect to Database
const dbURL = process.env.MONGO_URL
mongoose.connect(dbURL, {useUnifiedTopology: true, useNewUrlParser: true, useCreateIndex: true})
mongoose.connection.on('error', () => console.log('An error occurred from the database'))
mongoose.connection.once('open', () => console.log('Succesfully connected to the database'))

app.route('/').get(((req, res) => {
    console.log('HEY!')
    res.send('HEY')
}))

// Start Node server
app.listen(port, () => {
    console.log(`Listening on port: ${port}`)
})