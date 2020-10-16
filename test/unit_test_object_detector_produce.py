from manager.kafka_manager import ObjectDetectManager, TFConverterManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager


def main():
    object_manager = ObjectDetectManager(KafkaConfig.object_detector)
    object_manager.produce("{'test':1}")
    print("SEND MSG")


if __name__ == "__main__":
    main()
