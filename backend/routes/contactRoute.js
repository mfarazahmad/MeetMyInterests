const router = express('express').Router()
const Contact = require('../models/contactModel')

router.route('/saveContact').post((req, res) => {
    const data = req.body.payload
    const {name, contact_type, contact, availability, inquery_type, message} = data

    // Save data into database
    let newContact = new Contact({name, contact_type, contact, availability, inquery_type, message})
    newContact.save()
    .then(() => res.json({'status':'SUCCESS', 'msg':'Contact Data Saved!' }))
    .catch(err => res.status(400).json({'status': 'FAILED', 'msg':`Failed to save contact data: ${err}`}))
})

router.route('/messages').get((req, res) => {
    
    // Retreive messages
    Contact.find()
    .then(messages => res.json({'status':'SUCCESS', 'msg':'List of messages', 'data':messages}))
    .catch(err => res.status(400).json({'status':'FAILED', 'msg':`Failed to retreive contact data: ${err}`}))
})


module.exports = router