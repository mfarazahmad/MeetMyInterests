from kafka import KafkaConsumer
from json import loads
from config.logger import log

class Broker():
    def __init__(self, host:str, topic: str, group: str, timeout: int):
        log.info(f"Subscribing To Kafka Topic {topic} @ Host: {host}")
        self.consumer = KafkaConsumer(
            topic,                                  # Kafka Topic to Listen To
            bootstrap_servers=[host],
            auto_offset_reset='earliest',           # Ensures messages start from last commit      
            enable_auto_commit=True,                # Ensures reads are committed during interval
            auto_commit_interval_ms=1000,           # Interval for read commits
            group_id=group,                         # Consumer Group
            value_deserializer=lambda x: loads(x.decode('utf-8'))   # Puts Message Into JSON
        )
        self.topic = topic

    def listen(self):
        log.info(f'Listening for new messages topic {self.topic}')
        for message in self.consumer:
            log.info(f'New Message Incoming: {message.value}')