import time
import json
from manager.kafka_manager import ObjectDetectKafkaManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager


def main():
    docker_conf = DockerConfig.object_detector
    kafka_conf = KafkaConfig.object_detector
    object_detector = DockerManager(docker_conf)
    object_detect_kafka_manager = ObjectDetectKafkaManager(kafka_conf)

    while True:
        message = object_detect_kafka_manager.poll(
            timeout_ms=kafka_conf.consumer.consumer_timeout_ms,
            max_records=kafka_conf.consumer.max_records)
        if message:
            envs = {}
            for key, value in message.items():
                envs = json.loads(value[0].value)
                print(envs)

            object_detector.run(envs)
            # object_detect_kafka_manager.produce(envs)
        else:
            time.sleep(kafka_conf.consumer.sleep)


if __name__ == "__main__":
    main()
