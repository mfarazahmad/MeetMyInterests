import React, {useEffect, useState} from 'react';

import {Divider}  from 'antd';
import {Card} from 'antd';
import { Form, Button, Input, Select, Slider } from 'antd';

import {setOptions, dayOptions, movementTypeOptions,anatomyOptions, excerciseOptions, equipmentOptions} from '../../utils/constants';

const ProgramExcerciseForm = (props) => {
    return (
        <Card className='popoutForm' bordered={true} hidden={props.isexcerciseProgramVisible}>
            <Divider orientation="left">New Excercise</Divider>
            <Form onFinish={(values) => props.handleForm(values, 'programExcercise')}  className='programExcerciseForm'>
                
                <Form.Item label="Excercise" name="excercise">
                    <Select
                        showArrow
                        defaultValue={['0']}
                        style={{ width: '100%' }}
                        options={excerciseOptions}
                    />
                </Form.Item>

                <Form.Item label="Workout Day" name="workoutDay">
                    <Select
                        showArrow
                        defaultValue={['A']}
                        style={{ width: '100%' }}
                        options={dayOptions}
                    />
                </Form.Item>

                <Form.Item label="Equipment" name="equipment">
                    <Select
                        mode="multiple"
                        showArrow
                        defaultValue={['dumbell', 'bench']}
                        style={{ width: '100%' }}
                        options={equipmentOptions}
                    />
                </Form.Item>

                <Form.Item label="Body Part(s)" name="anatomy">
                    <Select
                        mode="multiple"
                        showArrow
                        defaultValue={['3', '2']}
                        style={{ width: '100%' }}
                        options={anatomyOptions}
                    />
                </Form.Item>


                <Form.Item label="Movement Type" name="movementType">
                    <Select
                        showArrow
                        defaultValue={['push']}
                        style={{ width: '100%' }}
                        options={movementTypeOptions}
                    />
                 </Form.Item>
                
                <Form.Item label="Recommended Sets" name="recommendedSets">
                    <Select
                        showArrow
                        defaultValue={['3']}
                        style={{ width: '100%' }}
                        options={setOptions}
                    />
                </Form.Item>

                <Form.Item label="Recommended Reps" name="recommendedReps">
                    <Slider defaultValue={12} min={1} max={40} />
                </Form.Item>

                <Form.Item label="Recommended Volume" name="volume">
                    <Input />
                </Form.Item>

                <Form.Item label="Band Weight Multiplier" name="bandMultiplier">
                    <Input />
                </Form.Item>

                <Form.Item label="Aternative Excercise" name="altExcercise">
                    <Select
                        showArrow
                        defaultValue={['13']}
                        style={{ width: '100%' }}
                        options={excerciseOptions}
                    />
                </Form.Item>


                <Button type="danger" htmlType="submit">Add</Button>
                
            </Form>
        </Card>

    );
}

export default ProgramExcerciseForm;