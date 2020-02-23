const router = require('express').Router()
const Contact = require('../models/contact_model')
const validContact = require('../validators/validContact')

router.route('/save').post((req, res) => {
    const data = req.body.payload
    const name, contact, contact_type, inquery, avail, desc = {...data}
    
    // Validate contact data
    validData = validContact(data)

    if (validData['status']) {
        
        // Save Contact Info in Database
        newContact = new Contact({
            name,
            contact,
            contact_type,
            inquery,
            avail,
            desc
        })

        newContact.save()
        .then(() => res.json({'status':'SUCCESS', 'msg': 'Saved Contact Data'}))
        .catch(err => res.status(400).json({'status':'FAILED', 'msg':'Failed to save contact!' + err}))
    } else {
        res.status(400).res.json({'status':'FAILED', 'msg':'Invalid form data!','errors':validData['errors'] })
    }
})

module.exports = router