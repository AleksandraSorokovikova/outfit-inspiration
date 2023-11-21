import pickle
from data.data import upload_file
from model_interface.image_similarity.config import (
    MODEL_INTERFACE_PATH,
    FEED_TEST,
    MODEL_PATH,
)
from model_interface.image_similarity.SimilarityModel import SimilarityModel
from model_interface.image_similarity.SimilarityModelInterface import (
    SimilarityModelInterface,
)


def train_and_save_model():
    model = SimilarityModel()
    model.init_layers()
    train, validation, test = model.feed_train_sets(feed_test=FEED_TEST)
    model.train(train, validation)
    model.save_model()


def save_model_interface():
    interface = SimilarityModelInterface()
    with open(MODEL_INTERFACE_PATH, "wb") as f:
        pickle.dump(interface, f)


def upload_models():
    upload_file(MODEL_PATH, "similarity_model_weights.h5")
    upload_file(MODEL_INTERFACE_PATH, "similarity_model_interface.pickle")


def flow():
    train_and_save_model()
    save_model_interface()
    upload_models()
