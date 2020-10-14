from kafka_manager import ObjectDetectManager, TFConverterManager
from config import KafkaConfig
from config import DockerConfig
from docker_manager import DockerManager

# manager = DockerManager(DockerConfig.object_detector)
# manager.run()

manager = DockerManager(DockerConfig.tflite_converter)
# manager.run()

object_manager = ObjectDetectManager(KafkaConfig.object_detector)
converter_manager = TFConverterManager(KafkaConfig.tflite_converter)
object_manager.produce("{'test':1}")
converter_manager.consume(manager)
