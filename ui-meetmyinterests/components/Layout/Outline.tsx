import React, { useEffect, useRef } from 'react'

import Navbar from './Navbar'

type Props = {
    children: JSX.Element
}

const Outline = (props: Props) => {

    return (
        <div className="outline">
            <Navbar />
            {props.children}
        </div>
    )
}

export default Outline;