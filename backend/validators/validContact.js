
// Validates contact data
function validContact(data) {
    validData = {'status':true, 'errors': []}
    const name, contact, contact_type, inquery, avail, desc = {...data}
    
    if (contact_type === 'phone') {
        if (contact.length !== 10) {
            validData['errors'].push({'contact':'Invalid Phone Length'})
        }
    } else if (contact_type === 'email') {
        if (contact.length < 6) {
            validData['errors'].push({'contact':'Invalid Email Length'})
        }
    }
    
    if (validData['errors'].length === 0) {
        validData['status'] = false
    }

    return validData
}

module.exports = validContact