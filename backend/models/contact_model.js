const mongoose = require('mongoose')

const Schema = mongoose.Schema
const contactSchema = new Schema({
    name:           {type:String, required:true, trim:true, minlength: 4},
    contact:        {type:String, required:false, trim:true, minlength: 6},
    contact_type:   {type:String, required:false, trim:true},
    inquery_type:   {type:String, required:true, trim:true},
    availability:   {type:String, required:true, trim:true},
    description:    {type:String, required:true, trim:true, minlength: 5}
},
    {timestamps: true}
)

const Contact = mongoose.model('Contact', contactSchema)

module.exports = Contact