from kafka_manager import ObjectDetectManager, TFConverterManager
from config import KafkaConfig
from config import DockerConfig
from docker_manager import DockerManager
import time


def main():
    object_detector = DockerManager(DockerConfig.object_detector)
    object_manager = ObjectDetectManager(KafkaConfig.object_detector)

    while True:
        time.sleep(1)
        object_manager.consume(object_detector)


if __name__ == "__main__":
    main()