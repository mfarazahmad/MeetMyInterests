import React from "react";
import { Timeline } from "antd";

const data = [
  { id: 1, name: "Greek Empire", year: "800 BC - 146 BC", description: "Flourished in Athens and surrounding areas." },
  { id: 2, name: "Macedonian Empire", year: "356 BC - 323 BC", description: "Expanded under Alexander the Great." },
  { id: 3, name: "Roman Empire", year: "27 BC - 476 AD", description: "Dominated the Mediterranean region." },
  { id: 4, name: "Byzantine Empire", year: "330 AD - 1453 AD", description: "Continued Roman traditions in the east." },
  { id: 5, name: "Islamic Caliphate", year: "622 AD - 1258 AD", description: "Spanned the Middle East and North Africa." },
  { id: 6, name: "Rightly Guided Caliphs", year: "632 AD - 661 AD", description: "Early Islamic leadership after Prophet Muhammad." },
  { id: 7, name: "Umayyad Dynasty", year: "661 AD - 750 AD", description: "Established Damascus as the capital." },
  { id: 8, name: "Abbasid Dynasty", year: "750 AD - 1258 AD", description: "Known for advancements in science and culture." },
  { id: 9, name: "Fatimid Caliphate", year: "909 AD - 1171 AD", description: "Centered in Cairo, Egypt." },
  { id: 10, name: "Seljuk Empire", year: "1037 AD - 1194 AD", description: "Spread Islamic culture and influence in Central Asia." },
  { id: 11, name: "Mongol Empire", year: "1206 AD - 1368 AD", description: "Largest contiguous empire in history." },
  { id: 12, name: "Ottoman Empire", year: "1299 AD - 1923 AD", description: "Controlled parts of Europe, Asia, and Africa." },
  { id: 13, name: "Mughal Empire", year: "1526 AD - 1857 AD", description: "Known for architectural achievements in India." },
  { id: 14, name: "Ethiopian Empire (Abyssinia)", year: "1270 AD - 1974 AD", description: "One of the oldest continuous monarchies." },
];

const timelineItems = data.map((item) => ({
  children: (
    <div>
      <h3>{item.name}</h3>
      <p>
        <strong>Years:</strong> {item.year}
      </p>
      <p>{item.description}</p>
    </div>
  ),
  color: "blue",
}));

const HistoricalTimeline = () => {
  return (
    <div style={{ padding: "5px" }}>
      <h1 style={{ textAlign: "center" }}>Historical Timeline</h1>
      <Timeline mode="alternate" items={timelineItems} />
    </div>
  );
};

export default HistoricalTimeline;
