import os

from data.data import get_and_save_files
from model_interface.image_similarity.config import (
    CLASSIFICATION_MODEL_PATH,
    SIMILARITY_MODEL_PATH,
    SIMILARITY_MODEL_NAME,
    CLASSIFICATION_MODEL_NAME,
)
import numpy as np
from keras.applications.resnet50 import preprocess_input
import onnxruntime as ort


class SimilarityModelInterface:
    @staticmethod
    def get_embeddings(images_array: list[np.ndarray]) -> np.ndarray:
        processed_images = np.array([preprocess_input(image) for image in images_array])
        session = ort.InferenceSession(SIMILARITY_MODEL_PATH)
        input_details = session.get_inputs()
        embeddings = session.run(None, {input_details[0].name: processed_images})
        return np.array(embeddings[0])

    @staticmethod
    def get_class(images_array: list[np.ndarray]) -> np.ndarray:
        session = ort.InferenceSession(CLASSIFICATION_MODEL_PATH)
        input_details = session.get_inputs()
        processed_images = np.array([preprocess_input(image) for image in images_array])
        predictions = session.run(None, {input_details[0].name: processed_images})
        classes = np.argmax(predictions[0], axis=1)
        return classes
