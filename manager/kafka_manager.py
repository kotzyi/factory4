import json
from kafka import KafkaProducer, KafkaConsumer
from bson import json_util


class KafkaManager:
    def __init__(self, conf):
        self.conf = conf
        self.producer = KafkaProducer(
            bootstrap_servers=conf.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x, default=json_util.default).encode('utf-8'))
        self.consumer = KafkaConsumer(
            bootstrap_servers=conf.bootstrap_servers,
            group_id=conf.consumer.consumer_group_id,
            consumer_timeout_ms=conf.consumer.consumer_timeout_ms,
            auto_offset_reset='smallest',
            enable_auto_commit=True,
            max_poll_interval_ms=3600000)
        self.consumer.subscribe(topics=conf.consumer.topics)

    def produce(self, value):
        self.producer.send(topic=self.conf.producer.topic, value=value)

    def poll(self, timeout_ms, max_records):
        return self.consumer.poll(timeout_ms=timeout_ms, max_records=max_records)

    def commit(self):
        self.consumer.commit()

    def close(self):
        self.consumer.close()
