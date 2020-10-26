import time
import json
from manager.kafka_manager import KafkaManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager


def main():
    docker_conf = DockerConfig.tflite_converter
    kafka_conf = KafkaConfig.tflite_converter
    tflite_converter = DockerManager(docker_conf)
    tflite_converter_kafka_manager = KafkaManager(kafka_conf)

    while True:
        message = tflite_converter_kafka_manager.poll(
            timeout_ms=kafka_conf.consumer.consumer_timeout_ms,
            max_records=kafka_conf.consumer.max_records)

        if message:
            envs = {}
            for key, value in message.items():
                envs = value[0].value
                print(envs)

            tflite_converter.run(envs)

            # tflite_converter_kafka_manager.produce(envs)
        else:
            time.sleep(kafka_conf.consumer.sleep)

if __name__ == "__main__":
    main()

