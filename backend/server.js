const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const dotenv = require('.dotenv')
const parse_json = require('parse-json')

const app = express.app()

app.use(cors)
app.use(mongoose)

const port = 7222;

const client = mongoose.Connection('127.0.0.1')

app.get('/', ((req, res) => {
    console.log('HEY!')
}))

app.listen((port) => {
    console.log(`Listening on port $("port")`)
})