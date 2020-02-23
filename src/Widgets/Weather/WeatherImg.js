
import WeatherImg from './Weather/WeatherImg'


function WeatherImg(props) {

    if (props.condition === 'Sunny') <img></img>
    else if (props.condition === 'Rainy') <img></img>
    else if (props.condition === 'Snowy') <img></img>
    else if (props.condition === 'Cloudy') <img></img>
    else if (props.condition === 'Foggy') <img></img>
    else { 
        return (
            <div className="MiniWeatherContainer">
                {props.weather['week'].map((data, index) => {
                    <div className="WeekForcast">
                        <WeatherImg condition={data['condition']}/>
                        <div className="CurrentDay" key={index}>{data['day']}</div>
                        <div className="CurrentTemp" key={index}>{data['temperature']}</div>
                        <div className="CurrentCondition" key={index}>{data['condition']}</div>
                        <div className="CurrentHigh" key={index}>{data['high']}</div>
                        <div className="CurrentLow" key={index}>{data['low']}</div>
                    </div>
                })}
            </div>
        )
    }
}

export default WeatherImg;