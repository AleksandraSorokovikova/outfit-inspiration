import os
os.environ["config"] = "dev"

from data.data import upload_file
from model_interface.image_similarity.config import (
    FEED_TEST,
    CLASSIFICATION_MODEL_PATH,
    CLASSIFICATION_MODEL_NAME,
    SIMILARITY_MODEL_PATH,
    SIMILARITY_MODEL_NAME,
    MODEL_NAME,
    MODEL_WEIGHTS
)
from model_interface.image_similarity.SimilarityModel import SimilarityModel


def train_and_save_model() -> None:
    model = SimilarityModel()
    model.init_layers()
    train, validation, test = model.feed_train_sets(feed_test=FEED_TEST)
    model.train(train, validation)
    model.save_model()
    model.save_onnx()


def upload_model() -> None:
    upload_file(path=CLASSIFICATION_MODEL_PATH, key=CLASSIFICATION_MODEL_NAME)
    upload_file(path=SIMILARITY_MODEL_PATH, key=SIMILARITY_MODEL_NAME)
    upload_file(path=MODEL_WEIGHTS, key=MODEL_NAME)


def flow() -> None:
    train_and_save_model()
    upload_model()


if __name__ == "__main__":
    flow()
