
// Validates contact data
function validContact(data) {
    validData = true;
    const name, contact, contact_type, inquery, avail, desc = {...data}
    if (contact_type === 'phone') {
        if (contact.length !== 10) {
            return false
        }
    } else if (contact_type === 'email') {
        if (contact.length < 6) {
            return false
        }
    }

    return validData
}

module.exports = validContact