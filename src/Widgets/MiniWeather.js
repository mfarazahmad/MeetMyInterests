
function MiniWeather(props) {
    return (
        <div className="MiniWeatherContainer">
            <ul>
                {props.weather.map((data, index) => {
                    <li key={index}>{data['temperature']}</li>
                })}
            </ul>
        </div>
    )
}

export default MiniWeather;