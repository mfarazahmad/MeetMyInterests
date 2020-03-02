const mongoose = require('mongoose')

const Schema = mongoose.Schema()

const contactSchema = new Schema(
    {
        name: {type: String, required: true, trim: true, minlength: 4},
        contact_type: {type: String, required: true, minlength: 6},
        contact: {type: String, required: true},
        availability: {type: String, required: true},
        inquery_type: {type:String, required: true},
        message: {type: String, required:true, minlength: 5},
    },
    {   timestamps: true}
)

const Contact = new mongoose.model('Contact', contactSchema)

module.exports = Contact