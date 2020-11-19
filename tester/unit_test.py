import unittest
from manager.config import KafkaConfig
import json
from kafka import KafkaProducer
from bson import json_util


class TestModelGeneration(unittest.TestCase):

    def test_produce_msg(self):
        msg = {}
        msg['FACTORY_ID'] = "233"
        msg['LEARN_ID'] = "252"
        msg['AZURE_SHARE_NAME'] = "model"
        msg['AZURE_IMAGE_DIR_PATH'] = "233/252/user"
        msg['AZURE_LABEL_DIR_PATH'] = "233/252/annotations"
        msg['AZURE_MODEL_DIR_PATH'] = "233/252/model"

        self.producer = KafkaProducer(
            bootstrap_servers=KafkaConfig.object_detector.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x, default=json_util.default).encode('utf-8'))

        self.producer.send(topic='REQ_CVT_TF_MDL', value=msg)


if __name__ == '__main__':
    unittest.main()

