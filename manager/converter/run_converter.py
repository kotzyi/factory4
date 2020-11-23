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

    docker_conf = DockerConfig.converter
    kafka_conf = KafkaConfig.converter
    converter = DockerManager(docker_conf)
    converter_kafka_manager = KafkaManager(kafka_conf)

    while True:
        message = converter_kafka_manager.poll(
            timeout_ms=kafka_conf.consumer.consumer_timeout_ms,
            max_records=kafka_conf.consumer.max_records)

        if message:
            envs = {}
            model_volumes = []
            topic = ""
            for key, value in message.items():
                envs = json.loads(value[0].value)
                topic = key.topic
            model_volumes.append([docker_conf.model_volume_by_topic[topic]])
            envs['MODEL_FILENAME_PREFIX'] = docker_conf.model_filename_prefix_by_topic[topic]

            logger.info(f"MSG RECEIVED")
            logger.info(f"TOPIC: {topic}")
            logger.info(f"CONSUMER_GROUP_ID: {kafka_conf.consumer.consumer_group_id}")
            logger.info(f"VALUES: {envs}")

            converter.add_env(envs)
            converter.add_volumes(model_volumes)
            converter.run()
            converter_kafka_manager.produce(envs)
        else:
            time.sleep(kafka_conf.consumer.sleep)


if __name__ == "__main__":
    main()
