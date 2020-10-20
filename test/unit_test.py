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
        msg = {}
        msg['AZURE_SHARE_NAME'] = 'models'
        msg['AZURE_DIR_PATH'] = 'test/1'
        json_msg = json.dumps(msg)

        self.producer = KafkaProducer(
            bootstrap_servers=KafkaConfig.object_detector.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x, default=json_util.default).encode('utf-8'))

        self.producer.send(topic='REQ_CVT_TF_MDL', value=json_msg)


if __name__ == '__main__':
    unittest.main()

