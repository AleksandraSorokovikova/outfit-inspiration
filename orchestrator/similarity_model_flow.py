import pickle
from data.data import upload_file
from model_interface.image_similarity.config import (
    MODEL_INTERFACE_PATH,
    FEED_TEST,
    MODEL_PATH,
    MODEL_NAME,
    MODEL_INTERFACE_NAME
)
from model_interface.image_similarity.SimilarityModel import SimilarityModel
from model_interface.image_similarity.SimilarityModelInterface import (
    SimilarityModelInterface,
)


def train_and_save_model() -> None:
    model = SimilarityModel()
    model.init_layers()
    train, validation, test = model.feed_train_sets(feed_test=FEED_TEST)
    model.train(train, validation)
    model.save_model()


def save_model_interface() -> None:
    interface = SimilarityModelInterface()
    with open(MODEL_INTERFACE_PATH, "wb") as f:
        pickle.dump(interface, f)


def upload_models() -> None:
    upload_file(path=MODEL_PATH, key=MODEL_NAME)
    upload_file(path=MODEL_INTERFACE_PATH, key=MODEL_INTERFACE_NAME)


def flow() -> None:
    train_and_save_model()
    save_model_interface()
    upload_models()


if __name__ == '__main__':
    flow()
