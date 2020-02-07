const router = require('express').Router()
const User = require('../models/user-model')

router.route('/').get((req, res) => {
    User.find()
    .then(users => res.json({'msg':'List of users', 'data': users}))
    .catch(err => res.status(400).json({'msg':'Error: ' + err}))
})

router.route('/login').post((req, res) => {
   const username = req.body.username
   const password = req.body.password

   User.findOne({username})
   .then(user => {
        if (user.password != password ) {
            res.json({'msg':`Invalid password!`})
        } else {
            res.json({'msg':'Login Succesful', 'data':'authToken=00521'})
        }
    })
   .catch(() => res.status(400).json({'msg':`Username ${username} does not exist!`}))
})

router.route('/addUser').post( (req, res) => {
    const username = req.body.username
    const password = req.body.password
    const email = req.body.email

    newUser = new User({
        username,
        password,
        email
    })

    newUser.save()
    .then(() => res.json({'msg':`New user ${username} saved!`}))
    .catch(err => res.status(400).json({'msg':'Failed to add user!: ' + err}))
})

module.exports = router