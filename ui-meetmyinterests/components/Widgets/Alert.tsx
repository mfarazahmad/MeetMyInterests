import React, { MouseEventHandler } from 'react';
import { Alert } from 'antd';

type Props = {
    alertVisible: boolean,
    successCheck: boolean
    successMsg: string,
    failedMsg: string,
    setAlertVisiblity: Function
}

const CustomAlert = (props: Props) => {

    const handleAlertClose = () => {
        props.setAlertVisiblity(false);
    };

    return (
        <div>
            {props.alertVisible && (
                props.successCheck ?
                    <Alert
                        message={props.successMsg}
                        type="success"
                        closable
                        afterClose={handleAlertClose}
                    /> :
                    <Alert
                        message={props.failedMsg}
                        type="error"
                        closable
                        afterClose={handleAlertClose}
                    />
            )
            }
        </div>
    )
}

export default CustomAlert;