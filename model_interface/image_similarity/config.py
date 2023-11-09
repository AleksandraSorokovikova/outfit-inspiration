import os

ORIG_INPUT_DATASET = "images_data"

BASE_PATH = "images_dataset"

TRAIN_PATH = os.path.sep.join([BASE_PATH, "train"])
VAL_PATH = os.path.sep.join([BASE_PATH, "validation"])
TEST_PATH = os.path.sep.join([BASE_PATH, "test"])

TRAIN_SPLIT = 0.8

INIT_LR = 1e-4
BATCH_SIZE = 128
NUM_EPOCHS = 5

NUMBER_OF_CLASSES = 17

MODEL_PATH = "images_similarity.model"

MODEL_INTERFACE_PATH = "images_similarity_interface.pickle"
