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
        self.producer.send(self.conf.producer.topic, value)

    def consume(self, docker_manager):
        pass

    def commit(self):
        self.consumer.commit()


class ObjectDetectManager(KafkaManager):
    def __init__(self, conf):
        super().__init__(conf)

    def consume(self, docker_manager):
        for msg in self.consumer:
            docker_manager.run()
            self.produce("{'test':1}")
            print("!!!!!!!!!!!!!")


class TFConverterManager(KafkaManager):
    def __init__(self, conf):
        super().__init__(conf)

    def consume(self, docker_manager):
        for msg in self.consumer:
            docker_manager.run()
            self.produce("{'test':2}")
            print("!!!!!!!!!!!!!")

