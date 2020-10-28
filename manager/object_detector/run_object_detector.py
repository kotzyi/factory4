import time
import json
import logging
from manager.kafka_manager import KafkaManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        level=logging.INFO,
    )

    docker_conf = DockerConfig.object_detector
    kafka_conf = KafkaConfig.object_detector
    object_detector = DockerManager(docker_conf)
    object_detect_kafka_manager = KafkaManager(kafka_conf)

    while True:
        message = object_detect_kafka_manager.poll(
            timeout_ms=kafka_conf.consumer.consumer_timeout_ms,
            max_records=kafka_conf.consumer.max_records)
        if message:
            envs = {}
            for key, value in message.items():
                envs = json.loads(value[0].value)

            logger.info(f"MSG RECEIVED")
            logger.info(f"TOPIC: {kafka_conf.consumer.topic}")
            logger.info(f"CONSUMER_GROUP_ID: {kafka_conf.consumer.consumer_group_id}")
            logger.info(f"VALUES: {envs}")

            object_detector.run(envs)
            object_detect_kafka_manager.produce(envs)
        else:
            time.sleep(kafka_conf.consumer.sleep)


if __name__ == "__main__":
    main()