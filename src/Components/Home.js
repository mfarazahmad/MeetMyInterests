import React, {Component} from 'react';


class Home extends Component(props) {
    constructor() {
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