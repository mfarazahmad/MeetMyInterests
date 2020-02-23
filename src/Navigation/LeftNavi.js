import React, {Component} from 'react';
import Logo from '../Widgets/Logo'
import MiniWeather from '../Widgets/MiniWeather'

class LeftNavi extends Component {
    constructor(props) {

        super(props);
        this.state ={};
        
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        console.log(e);
    }

    render() {
        return (
            <div>
                <Logo />
                <MiniWeather />
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