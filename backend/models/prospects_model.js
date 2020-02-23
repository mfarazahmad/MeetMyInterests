const mongoose = require('mongoose')

const Schema = mongoose.Schema 
const jobSchema = new Schema({
    job:        {type:String, required:true, trim:true, minlength: 4 },
    contact:    {type:String, required:true, trim:true, minlength: 4 },
    notes:      {type:String, required:true, trim:true, minlength: 10 }
}, 
    {timestamps: true}
)

const Prospects = mongoose.model('Prospects', jobSchema)

module.exports = Prospects