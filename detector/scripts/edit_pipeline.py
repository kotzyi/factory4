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
    num_classes = int(os.getenv('NUM_CLASSES'))
    image_size = int(os.getenv('IMAGE_SIZE'))
    batch_size = int(os.getenv('BATCH_SIZE'))
    total_step = int(os.getenv('TOTAL_STEP'))
    num_boxes = int(os.getenv('NUM_BOXES'))
    replicas_to_aggregate = int(os.getenv('REPLICAS_TO_AGGREGATE'))
    model_type = os.getenv('MODEL_TYPE')
    warmup_step = int(os.getenv('WARMUP_STEP'))
    classification_weight = float(os.getenv("CLASSIFICATION_WEIGHT"))
    localization_weight = float(os.getenv("LOCALIZATION_WEIGHT"))

    pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()

    with tf.gfile.GFile(pipeline, "r") as f:
        proto_str = f.read()
        text_format.Merge(proto_str, pipeline_config)

    pipeline_config.train_config.fine_tune_checkpoint = os.path.join(pre_trained_model_path, "checkpoint/ckpt-0")
    pipeline_config.train_input_reader.label_map_path = os.getenv('TRAIN_IMAGE_LABEL_PATH')
    pipeline_config.train_input_reader.tf_record_input_reader.input_path[0] = os.getenv('TRAIN_IMAGE_TFRECORD_PATH')

    model_config = pipeline_config.model.ssd
    model_config.num_classes = num_classes
    model_config.image_resizer.keep_aspect_ratio_resizer.min_dimension = image_size
    model_config.image_resizer.keep_aspect_ratio_resizer.max_dimension = image_size
    model_config.loss.classification_weight = classification_weight
    model_config.loss.localization_weight = localization_weight

    train_config = pipeline_config.train_config
    train_config.fine_tune_checkpoint_type = model_type
    train_config.data_augmentation_options[0].random_scale_crop_and_pad_to_square.output_size = image_size
    train_config.batch_size = batch_size
    train_config.num_steps = total_step
    train_config.replicas_to_aggregate = replicas_to_aggregate
    train_config.max_number_of_boxes = num_boxes
    train_config.use_bfloat16 = False

    optimizer_config = pipeline_config.train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate
    optimizer_config.total_steps = total_step
    optimizer_config.warmup_steps = warmup_step

    pipeline_config.eval_input_reader[0].label_map_path = os.getenv('TEST_IMAGE_LABEL_PATH')
    pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[0] = os.getenv('TEST_IMAGE_TFRECORD_PATH')

    config_text = text_format.MessageToString(pipeline_config)

    os.makedirs(os.path.dirname(edited_pipeline), exist_ok=True)

    with tf.gfile.Open(edited_pipeline, "wb+") as f:
        f.write(config_text)


if __name__ == '__main__':
    main()
