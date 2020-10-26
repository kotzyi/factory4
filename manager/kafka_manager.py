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
            value_deserializer=lambda x: json.loads(x.decode('utf-8'), object_hook=json_util.object_hook),
            consumer_timeout_ms=conf.consumer.consumer_timeout_ms,
            auto_offset_reset='smallest',
            enable_auto_commit=True,
            max_poll_interval_ms=3600000)
        self.consumer.subscribe(topics=conf.consumer.topic.split(','))

    def produce(self, value):
        self.producer.send(topic=self.conf.producer.topic, value=value)

    def consume(self, docker_manager):
        for msg in self.consumer:
            docker_manager.run()
            self.produce("{'test':2}")

    def poll(self, timeout_ms, max_records):
        return self.consumer.poll(timeout_ms=timeout_ms, max_records=max_records)

    def commit(self):
        self.consumer.commit()

    def close(self):
        self.consumer.close()

    def on_send_success(record_metadata):
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    def on_send_error(excp):
        print('I am an errback')