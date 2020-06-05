
import React, {Component} from 'react';
import WeatherImg from './WeatherImg'

class LargeWeather extends Component{

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
                <div className="Today">
                    <WeatherImg condition={this.state.weatherData['today']['condition']}/>
                    <div className="CurrentDay" key={index}>{this.state.weatherData['today']['day']}</div>
                    <div className="CurrentTemp" key={index}>{this.state.weatherData['today']['temperature']}</div>
                    <div className="CurrentCondition" key={index}>{this.state.weatherData['today']['condition']}</div>
                    <div className="CurrentHigh" key={index}>{this.state.weatherData['today']['high']}</div>
                    <div className="CurrentLow" key={index}>{this.state.weatherData['today']['low']}</div>
                </div>
            {this.state.weatherData && this.state.weatherData['week'].map((data, index) => {
                return (
                    <div className="WeekForcast">
                        <WeatherImg condition={data['condition']}/>
                        <div className="CurrentDay" key={index}>{data['day']}</div>
                        <div className="CurrentTemp" key={index}>{data['temperature']}</div>
                        <div className="CurrentCondition" key={index}>{data['condition']}</div>
                        <div className="CurrentHigh" key={index}>{data['high']}</div>
                        <div className="CurrentLow" key={index}>{data['low']}</div>
                    </div>
                 );
            })}
            </div>
        );
    }
}

export default LargeWeather;