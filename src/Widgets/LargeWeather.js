
import React, {Component} from 'react';

class LargeWeather {

    constructor(props) {

        super(props);
        this.state = {
            weatherData: this.props.weather
        };

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange() {
        console.log('HEY CHANGE!')
    }

    render() {
        return (
            <div className="LgWeatherContainer">
                <ul>
                    {props.weather.map((data, index) => {
                        <li key={index}>{data['temperature']}</li>
                    })}
                </ul>
            </div>
        )
    }
}

export default LgWeather;LargeWeather