import os

dev_path = "../files/"
prod_path = "../temp_files/"

env = os.getenv("config", "dev")
if env == "dev":
    base_path = dev_path
else:
    base_path = prod_path

ORIG_INPUT_DATASET = f"{base_path}images_polyvore_data"
IMAGES_DESCRIPTION_PATH = f"{base_path}images_caption_polyvore.csv"

BASE_PATH = f"{base_path}images_polyvore_dataset"

TRAIN_PATH = os.path.sep.join([BASE_PATH, "train"])
VAL_PATH = os.path.sep.join([BASE_PATH, "validation"])
TEST_PATH = os.path.sep.join([BASE_PATH, "test"])

TRAIN_SPLIT = 0.9
VALIDATION_SPLIT = 1

FEED_TEST = not (VALIDATION_SPLIT == 1)

INIT_LR = 1e-4
BATCH_SIZE = 128
NUM_EPOCHS = 5

NUMBER_OF_CLASSES = 8

IMAGE_SIZE = (224, 224)

MODEL_WEIGHTS = f"{base_path}images_similarity.h5"
MODEL_NAME = "images_similarity.h5"

SIMILARITY_MODEL_PATH = f"{base_path}similarity_model.onnx"
CLASSIFICATION_MODEL_PATH = f"{base_path}classification_model.onnx"

SIMILARITY_MODEL_NAME = "similarity_model.onnx"
CLASSIFICATION_MODEL_NAME = "classification_model.onnx"

