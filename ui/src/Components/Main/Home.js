import React, {Component} from 'react';


class Home extends Component {
    constructor(props) {

        super(props);
        
        this.state= {};

        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e) {
        console.log(e);
    }

    render() {
        return (
            <div onClick={this.handleChange}>Welcome to the home page!</div>
        );
    }
}

export default Home;