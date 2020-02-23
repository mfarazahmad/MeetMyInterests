import React, {Component} from 'react';
import axios from 'axios';
import Logo from '../Widgets/Logo'
import MiniWeather from '../Widgets/MiniWeather'
import Axios from 'axios';

class LeftNavi extends Component {
    constructor(props) {

        super(props);
        this.state ={};
        
        this.handleChange = this.handleChange.bind(this);
        this.getWeatherData = this.getWeatherData.bind(this);
    }

    handleChange(e) {
        console.log(e);
    }

    getWeatherData() {
        let weatherData = [];
        
        axios.get('www.google.com')
        .then((resp) => {   
                conmsole.log(resp.data);
                weatherData = resp.data;
            })
        .catch((err) => {
                console.log(err);
        });

        return weatherData;
    }

    render() {
        return (
            <div>
                <Logo />
                <MiniWeather weather={this.getWeatherData}/>
                <div className="NaviLinks">
                    <div>Home</div>
                    <div>Portfolio</div>
                    <div>Contact</div>
                    <div>Dashboard</div>
                </div>
            </div>
        );
    }
}

export default LeftNavi;