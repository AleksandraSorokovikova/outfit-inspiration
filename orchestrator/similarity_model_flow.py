import pickle
from data.data import upload_file
from model_interface.image_similarity.config import MODEL_INTERFACE_PATH
from model_interface.image_similarity.SimilarityModel import SimilarityModel
from model_interface.image_similarity.SimilarityModelInterface import SimilarityModelInterface


def train_and_save_model():
    model = SimilarityModel()
    model.init_layers()
    train, validation, test = model.feed_train_sets()
    model.train(train, validation)
    model.feed_similarity_model()
    model.save_model()


def save_model_interface():
    interface = SimilarityModelInterface()
    with open(MODEL_INTERFACE_PATH, 'wb') as f:
        pickle.dump(interface, f)


def upload_model_interface():
    upload_file(MODEL_INTERFACE_PATH, 'similarity_model_interface.pickle')


def flow():
    train_and_save_model()
    save_model_interface()
    upload_model_interface()
