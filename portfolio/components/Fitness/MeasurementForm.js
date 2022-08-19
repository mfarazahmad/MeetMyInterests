import React, {useEffect, useState} from 'react';

import {Card} from 'antd';
import { Form, Button, Input } from 'antd';

const MeasurementForm = (props) => {
    
    return (
        <Card className='popoutForm' bordered={true} >
            <Form onFinish={(values) => props.handleForm(values, 'measurement')}  className='measurementTrackerForm'>

                <Form.Item label="Height" name="height">
                    <Input />
                </Form.Item>

                <Form.Item label="Chest" name="chest">
                    <Input />
                </Form.Item>

                <Form.Item label="Bicep" name="bicep">
                    <Input />
                </Form.Item>

                <Form.Item label="Tricep" name="tricep">
                    <Input />
                </Form.Item>

                <Form.Item label="Thighs" name="thighs">
                    <Input />
                </Form.Item>

                <Form.Item label="Calves" name="calves">
                    <Input />
                </Form.Item>
                
                <Form.Item label="Waist" name="waist">
                    <Input />
                </Form.Item>

                <Form.Item label="Neck" name="neck">
                    <Input />
                </Form.Item>

                <Button type="primary" htmlType="submit">Save</Button>
                
            </Form>
        </Card>

    );
}

export default MeasurementForm;