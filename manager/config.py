from yaml2object import YAMLObject


class KafkaConfig(metaclass=YAMLObject):
    source = 'config.yaml'
    namespace = 'kafka'

class DockerConfig(metaclass=YAMLObject):
    source = 'config.yaml'
    namespace = 'docker'

