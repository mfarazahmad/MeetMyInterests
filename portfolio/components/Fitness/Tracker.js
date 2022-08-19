import React, {useEffect, useState} from 'react';

import {Col, Row, Divider, Collapse}  from 'antd';
import {Tag, List} from 'antd';

const { Panel } = Collapse;

import ExcerciseLogForm from './ExcerciseLogForm';
import MeasurementForm from './MeasurementForm';

import {excerciseData} from '../../utils/constants';


const Tracker = (props) => {

    const [dailyTrackerInfo, setDailyTracker] = useState([]);

    return (
        <div className='tracker'>
            <h3 style={{fontWeight: 'bold'}}>Log Today's Activities</h3>
            <Row gutter={16}>
                <Col span={8}>
                    <Divider orientation="left">Measurements</Divider>
                    <MeasurementForm />
                </Col>
                <Col span={8}>
                    <Divider orientation="left">Excercises</Divider>
                    <List
                        className='excercises'
                        size="small"
                        bordered
                        dataSource={excerciseData}
                        renderItem={(item, key) => (
                            <List.Item> 
                                <Tag color="red">Push</Tag> 
                                {item}
                                <br />
                                <Collapse ghost>
                                    <Panel header="Log" key={key} style={{'backgroundColor': 'orange', 'color': 'white'}}>
                                        <ExcerciseLogForm equipment={item.equipment} mulitiplier={item.band_multiplier} />
                                    </Panel>
                                </Collapse>
                            </List.Item>
                            )}
                    />
                </Col>
            </Row>
        </div>
    )
}

export default Tracker;