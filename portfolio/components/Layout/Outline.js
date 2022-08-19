import React, {useEffect, useRef} from 'react'

import Navbar from './Navbar'

const Outline = (props) => {

    return (
        <div className="outline">
            <Navbar />
            {props.children}
        </div>
    )
}

export default Outline;