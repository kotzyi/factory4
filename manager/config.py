import os
from yaml2object import YAMLObject


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class KafkaConfig(metaclass=YAMLObject):
    source = os.path.join(ROOT_DIR, 'config.yaml')
    namespace = 'kafka'

class DockerConfig(metaclass=YAMLObject):
    source = os.path.join(ROOT_DIR, 'config.yaml')
    namespace = 'docker'

