from manager.kafka_manager import ObjectDetectKafkaManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager
import time


def main():
    object_detector = DockerManager(DockerConfig.object_detector)
    object_detect_kafka_manager = ObjectDetectKafkaManager(KafkaConfig.object_detector)

    while True:
        message = object_detect_kafka_manager.poll(0)
        if message:
            print(message)
            object_detector.run()
            object_detect_kafka_manager.produce("{'test':2}")
        else:
            time.sleep(10)


if __name__ == "__main__":
    main()
