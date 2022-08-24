import React, {useEffect, useState} from 'react';

import { Card} from 'antd';
import { Form, Button, Input, Select, Slider } from 'antd';

import {setOptions} from '../../utils/constants';

const ExcerciseLogForm = (props) => {

    const bandSelector = (bandInfo, mulitiplier) => {
        const bandOptions = [];
        bandInfo.map(item => bandOptions.push({label: item.name, value: item.singleWeight * mulitiplier}) )
        return bandOptions;
    }

    return (
        <Card className='popoutForm' bordered={true} >
            <Form onFinish={(values) => props.handleForm(values, 'excerciseLog')}  className='excerciseTrackerForm'>

                <Form.Item label="Program" name="programID" style={{'display': 'none'}}>
                    <Input value={props.programID} disabled={true} />
                </Form.Item>

                <Form.Item label="Excercise" name="excerciseID" style={{'display': 'none'}}>
                    <Input value={props.excerciseID} disabled={true} />
                </Form.Item>
                
                <Form.Item label="Sets" name="set">
                    <Select
                        showArrow
                        defaultValue={['3']}
                        style={{ width: '100%' }}
                        options={setOptions}
                    />
                </Form.Item>
                
                <Form.Item label="Reps" name="reps">
                    <Slider defaultValue={12} min={1} max={40} />
                </Form.Item>

                {props.equipment && props.equipment.includes('Bands') ? (
                    <Form.Item label="Weight" name="weight">
                        <Select
                            showArrow
                            style={{ width: '100%' }}
                            options={() => bandSelector(props.equipment.bands, props.mulitiplier)}
                        />
                    </Form.Item>
                ) : (
                    <Form.Item label="Weight" name="weight">
                        <Input />
                    </Form.Item>
                )}

                <Button type="primary" htmlType="submit">Save</Button>
                
            </Form>
        </Card>

    );
}

export default ExcerciseLogForm;