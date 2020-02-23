
import WeatherImg from './WeatherImg'


function MiniWeather(props) {
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

export default MiniWeather;