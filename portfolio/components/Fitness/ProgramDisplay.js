import React, {useEffect, useState} from 'react';

import {Col, Row, Tabs}  from 'antd';
import {Card, Descriptions, Tag} from 'antd';
import {Button, Select} from 'antd';

import {anatomyOptions, excerciseOptions, excerciseTypeOptions, programOptions} from '../../utils/constants';


const ProgramDisplay = (props) => {

    const [programSelection, setProgram] = useState('0');

    const handleProgramSelection = e => {
        console.log('New Program Selected');
        setProgram(e)
    }

    return (
        <div className='displayData'>
            <Row gutter={16}>
                <Col span={16}>
                    <Descriptions title="Program Info" bordered>
                        <Descriptions.Item label="Workout Name">
                            <Select
                                showArrow
                                style={{ width: '100%' }}
                                value={programSelection}
                                options={programOptions}
                                onChange={handleProgramSelection}
                            />
                            <Button onClick={props.toggleProgramForm}>New</Button>
                        </Descriptions.Item>
                    </Descriptions>
                    {props.programsInfo && props.programsInfo.length > 0 && (
                    <Descriptions bordered>
                        <Descriptions.Item label="Workout Type">{props.programsInfo[programSelection]['excerciseType'] ? excerciseTypeOptions[props.programsInfo[programSelection]['excerciseType']]['label'] : 'N/A'}</Descriptions.Item>
                        <Descriptions.Item label="Frequency">{props.programsInfo[programSelection]['frequency']}</Descriptions.Item>
                        <Descriptions.Item label="Workout Routine"> 
                            <Tabs defaultActiveKey="1" type="card" >
                            {props.programsInfo[programSelection]['programExcercises'].length > 0 && props.programsInfo[programSelection]['programExcercises'].map( (item, key) => (
                                <TabPane tab={item.excercise ? excerciseOptions[item.excercise]['label'] : ''} key={key}>
                                    <Card title={item.excercise ? excerciseOptions[item.excercise]['label'] : ''} bordered={true}>
                                        <li> <Tag color="red">{item.movementType ? item.movementType : ''}</Tag> </li>

                                        <li> <em>Anatomy</em>: {item.anatomy && item.anatomy.length > 0 ? 
                                            item.anatomy.map( (anatomyItems, key) => (
                                                <Tag color="green">{anatomyOptions[anatomyItems]['label']} </Tag>
                                            ))   : 'N/A' } 
                                        </li>
                                        <li> <em>Recommended Volume</em>: {item.volume} | <em>Recommended Sets</em> {item.recommendedSets} |  <em>Recommended Reps</em>{item.recommendedReps} </li>
                                        <li> <em>Alternative Excercise</em>: {item.altExcercise ? excerciseOptions[item.altExcercise]['label'] : 'N/A' } </li>
                                        
                                        <li> <em>Equipment</em>: {item.equipment && item.equipment.length > 0 ? 
                                            item.equipment.map( (equipmentItems, key) => (
                                                <Tag color="blue">{equipmentItems} </Tag>
                                            ))   : 'N/A' } 
                                        </li>
                                    </Card>
                                </TabPane>
                            ))}
                            </Tabs>
                        </Descriptions.Item>
                    </Descriptions>
                    )}
                </Col>
            </Row>
        </div>


    );
}

export default ProgramDisplay;