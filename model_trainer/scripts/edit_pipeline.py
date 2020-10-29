import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import tensorflow.compat.v1 as tf
from google.protobuf import text_format
from object_detection.protos import pipeline_pb2


def main():
    pre_trained_model_root_path = os.getenv('PRE_TRAINED_MODEL_PATH')
    model_name = os.getenv('MODEL_NAME')
    pre_trained_model_path = os.path.join(pre_trained_model_root_path, model_name)
    pipeline = os.path.join(pre_trained_model_path, "pipeline.config")
    edited_pipeline = os.getenv('MODEL_PIPELINE_CONFIG_PATH')

    pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()

    with tf.gfile.GFile(pipeline, "r") as f:
        proto_str = f.read()
        text_format.Merge(proto_str, pipeline_config)


    pipeline_config.train_config.fine_tune_checkpoint = os.path.join(pre_trained_model_path, "checkpoint/ckpt-0")
    pipeline_config.train_input_reader.label_map_path = os.getenv('TRAIN_IMAGE_LABEL_PATH')
    pipeline_config.train_input_reader.tf_record_input_reader.input_path[0] = os.getenv('TRAIN_IMAGE_TFRECORD_PATH')

    pipeline_config.model.ssd.num_classes = 1
    pipeline_config.model.ssd.image_resizer.keep_aspect_ratio_resizer.min_dimension = 320
    pipeline_config.model.ssd.image_resizer.keep_aspect_ratio_resizer.max_dimension = 320
    pipeline_config.train_config.batch_size = 8
    pipeline_config.train_config.num_steps = 1000
    pipeline_config.train_config.max_number_of_boxes = 10
    pipeline_config.train_config.use_bfloat16 = False

    optimizer_config = pipeline_config.train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate
    optimizer_config.total_steps = 1000
    optimizer_config.warmup_steps = 100

    config_text = text_format.MessageToString(pipeline_config)
    print(config_text)
    with tf.gfile.Open(edited_pipeline, "wb") as f:
        f.write(config_text)


if __name__ == '__main__':
    main()
