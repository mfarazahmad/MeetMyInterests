import React, {Component} from 'react';


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
            <div onClick={this.handleChange}>Heyyyy</div>
        );
    }
}

export default LeftNavi;