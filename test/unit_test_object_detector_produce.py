import unittest
from manager.kafka_manager import ObjectDetectKafkaManager, TFConverterKafkaManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager
import json
from kafka import KafkaProducer, KafkaConsumer
from bson import json_util


class TestStringMethods(unittest.TestCase):

    def test_produce_msg(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KafkaConfig.object_detector.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x, default=json_util.default).encode('utf-8'))

        self.producer.send(topic='RESP_CVT_TF_MDL', value='{"test":1}')


if __name__ == '__main__':
    unittest.main()

