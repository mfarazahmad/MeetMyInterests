import React from "react";

import styles from '../styles/History.module.css';
import Outline from '../components/Layout/Outline';
import HistoricalMap from "../components/History/HistoricalMap";
import HistoricalTimeline from "../components/History/HistoricalTimeline";

const History = () => (
    <Outline>
        <div className={styles.main}>
            <h1 className={styles.header}>HISTORICAL WORLD MAP</h1>
            <div style={{ height: "400px" }}>
                <HistoricalMap />
            </div>
            <div style={{ height: "100%", overflow: "scroll" }}>
                <HistoricalTimeline />
            </div>
        </div>
    </Outline>

);

export default History;