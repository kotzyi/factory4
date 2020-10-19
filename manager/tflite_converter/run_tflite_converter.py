from manager.kafka_manager import TFConverterKafkaManager
from manager.config import KafkaConfig
from manager.config import DockerConfig
from manager.docker_manager import DockerManager
import time


def main():
    tflite_converter = DockerManager(DockerConfig.tflite_converter)
    tflite_converter_kafka_manager = TFConverterKafkaManager(KafkaConfig.tflite_converter)

    while True:
        message = tflite_converter_kafka_manager.poll(0)
        if message:
            print(message)
            tflite_converter.run()
            tflite_converter_kafka_manager.produce("{'test':2}")
        else:
            time.sleep(10)

    converter_manager.close()


if __name__ == "__main__":
    main()
