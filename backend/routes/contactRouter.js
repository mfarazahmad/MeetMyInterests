const router = require('express').Router()
const Contact = require('../models/contact_model')


router.route('/save').post((req, res) => {
    const data = req.body.data
})

module.exports = router