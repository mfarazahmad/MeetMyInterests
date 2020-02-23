const nodemailer = require('nodemailer')

// Create Mail Transporters
function createTransporter() {

    const transport = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            username: process.env.MAIL_USER,
            password: process.env.MAIL_PASS
        }
    })

    return transport
}

// Send Mail With Custom Template
function gotMail(template, data) {
   const transport = createTransporter()

   let subject = ''
   let body = ''

   if (template === 'contact_template') {
       subject = 'Contact Form Submission'
       body = `
            <h1>${data['inquery']}</h1>
            <p>${data['name']}</p>
            <p>${data['contact']}</p>
            <p>${data['desc']}</p>
            <p>${data['avail']}</p>
        `
   }

   const mailOptions = {
        from: process.env.MAIL_USER,
        to: process.env.MAIN_EMAIL,
        subject: subject,
        html: body
    }

   transport.sendMail(mailOptions, (error, info) => {
        if (error) console.log(error)
        else console.log(`Email sent: ${info.response}`)
    })
}


module.exports = gotMail