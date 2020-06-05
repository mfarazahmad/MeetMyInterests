import React, {Component} from 'react';
import axios from 'axios';
import Logo from '../Widgets/Logo'
import MiniWeather from '../Widgets/Weather/MiniWeather'

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
        let weatherData = {'week':[], 'today':{} };
        
        let detailedUrl = '';
        let url = 'https://api.weather.gov/points/33.76,-84.43';
        axios.get(url)
            .then((resp) => {   
                    console.log(resp);
                    console.log(resp.data['properties']['forecast']);
                    detailedUrl = resp.data['properties']['forecast'];

                    axios.get(detailedUrl)
                        .then((resp) => {   
                            console.log(resp.data);
                            let weekData = resp.data['properties']['periods'];
                            weatherData['week'] = weekData;
                            weatherData['today'] = weekData[0];
                        });
                })
            .catch((err) => {console.log(err); });

        return weatherData;
    }

    render() {
        return (
            <div>
                <Logo />
                <MiniWeather weather={this.getWeatherData()}/>
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