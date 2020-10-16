from kafka_manager import ObjectDetectManager, TFConverterManager
from config import KafkaConfig
from config import DockerConfig
from docker_manager import DockerManager
import time


def main():
    tflite_converter = DockerManager(DockerConfig.tflite_converter)
    converter_manager = TFConverterManager(KafkaConfig.tflite_converter)

    while True:
        time.sleep(1)
        converter_manager.consume(tflite_converter)


if __name__ == "__main__":
    main()