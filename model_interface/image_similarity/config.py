import os

ORIG_INPUT_DATASET = "images_data"

BASE_PATH = "images_dataset"

TRAIN_PATH = os.path.sep.join([BASE_PATH, "train"])
VAL_PATH = os.path.sep.join([BASE_PATH, "validation"])
TEST_PATH = os.path.sep.join([BASE_PATH, "test"])

TRAIN_SPLIT = 0.9
VALIDATION_SPLIT = 1

FEED_TEST = not (VALIDATION_SPLIT == 1)

INIT_LR = 1e-4
BATCH_SIZE = 128
NUM_EPOCHS = 5

NUMBER_OF_CLASSES = 17

IMAGE_SIZE = (224, 224)

MODEL_PATH = "images_similarity.h5"

MODEL_INTERFACE_PATH = "images_similarity_interface.pickle"

MODEL_CLASSES = {
    0: 'Blouses_Shirts',
    1: 'Cardigans',
    2: 'Denim',
    3: 'Dresses',
    4: 'Graphic_Tees',
    5: 'Jackets_Coats',
    6: 'Jackets_Vests',
    7: 'Leggings',
    8: 'Pants',
    9: 'Rompers_Jumpsuits',
    10: 'Shirts_Polos',
    11: 'Shorts',
    12: 'Skirts',
    13: 'Suiting',
    14: 'Sweaters',
    15: 'Sweatshirts_Hoodies',
    16: 'Tees_Tanks'
}
