from kafka import KafkaProducer, KafkaConsumer
import json

class Producer:
    def __init__(self, topic: str):
        self.kafka = KafkaProducer(bootstrap_servers='kafka:9092',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic

    def send(self, message: dict) -> None:
        self.kafka.send(self.topic, message)
        self.kafka.flush()

