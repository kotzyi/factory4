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
        msg['AZURE_SHARE_NAME'] = "models"
        msg['AZURE_CLASS_IMAGE_DIR_PATH'] = "detach/train_images"
        msg['AZURE_OBJECT_IMAGE_DIR_PATH'] = "detach/images"
        msg['AZURE_LABEL_DIR_PATH'] = "detach/annotations"
        msg['AZURE_MODEL_DIR_PATH'] = "detach/models"
        msg['CLASSIFIER_MODEL_NAME'] = "b0"
        msg['DETECTOR_MODEL_NAME'] = "efficientdet_d0_coco17_tpu-32"

        self.producer = KafkaProducer(
            bootstrap_servers=KafkaConfig.detector.bootstrap_servers,
            value_serializer=lambda x: json.dumps(x, default=json_util.default).encode('utf-8'))

        self.producer.send(topic='REQ_CVT_TF_MDL', value=msg)


if __name__ == '__main__':
    unittest.main()

