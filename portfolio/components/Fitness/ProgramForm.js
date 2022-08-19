import React, {useEffect, useState} from 'react';

import {Col, Row}  from 'antd';
import {Card, Modal} from 'antd';
import {Form, Button, Input, Select} from 'antd';

import ProgramExcerciseForm from './ProgramExcerciseForm';
import { frequencyOptions, excerciseTypeOptions} from '../../utils/constants';

const ProgramForm = (props) => {

    return (
        <Modal
            title="Add New Program"
            centered
            visible={props.isProgramVisible}
            onCancel={props.toggleProgramForm}
            footer={[]}
        >
            <Row gutter={26}>
                <Col span={12}>
                    <Card className='popoutForm' bordered={true} >
                        <Form onFinish={(values) => props.handleForm(values, 'program')} className='programForm'>

                            <Form.Item label="Program Name" name="programName">
                                <Input />
                            </Form.Item>

                            <Form.Item label="Excercise Type" name="excerciseType">
                                <Select
                                    showArrow
                                    style={{ width: '100%' }}
                                    options={excerciseTypeOptions}
                                />
                            </Form.Item>

                            <Form.Item label="Frequency" name="frequency">
                                <Select
                                    showArrow
                                    style={{ width: '100%' }}
                                    options={frequencyOptions}
                                />
                            </Form.Item>

                            <Button onClick={props.toggleExcerciseProgramForm}>Add Excercise</Button>
                            <Button type="primary" htmlType="submit">Save</Button>
                            
                        </Form>

                    </Card>
                </Col>
                <Col span={12}>
                    {props.newProgramExcercises.map((item, key) => (
                        <Card label={`Workout ${key}`}>
                            <li><strong>Excercise:</strong> {item['excercise']}</li>
                            <li><strong>Sets:</strong> {item['recommendedSets']}</li>
                            <li><strong>Reps:</strong> {item['recommendedReps']}</li>
                            <li><strong>Type:</strong>  {item['movementType']}</li>
                            <li><strong>Equipment:</strong>  {item['equipment']}</li>
                            <li><strong>Multi:</strong>  {item['bandMultiplier']}</li>
                            <li><strong>Anatomy:</strong>  {item['anatomy']}</li>
                            <li><strong>Workout Day:</strong>  {item['workoutDay']}</li>
                            <li><strong>Volume:</strong>  {item['volume']}</li>
                            <li><strong>Alt:</strong> {item['altExcercise']}</li>
                        </Card>
                    ))}
                </Col>

            </Row>
            <Row>
                <ProgramExcerciseForm handleForm={props.handleForm} isexcerciseProgramVisible={props.isexcerciseProgramVisible} />
            </Row>
        </Modal>

    );
}

export default ProgramForm