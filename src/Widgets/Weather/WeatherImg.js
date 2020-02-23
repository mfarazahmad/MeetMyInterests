import React from 'react';

function WeatherImg(props) {

    if (props.condition === 'Sunny') return <img></img>;
    else if (props.condition === 'Rainy') return <img></img>;
    else if (props.condition === 'Snowy') return <img></img>;
    else if (props.condition === 'Cloudy') return <img></img>;
    else if (props.condition === 'Foggy') return <img></img>;
    else return <div> Image can't be loaded...</div>;
}

export default WeatherImg;