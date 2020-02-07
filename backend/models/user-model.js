const mongoose = require('mongoose')

const Schema = mongoose.Schema
const userSchema = new Schema({
    username: {type:String, required: true, unique: true, trim: true, minLength: 3},
    password: {type:String, required: true, trim: true, minLength: 3},
    email: {type:String, required: true, trim: true, minLength: 5},
},
    {timestamps: true}
)

const User = mongoose.model('Users', userSchema)

module.exports = User