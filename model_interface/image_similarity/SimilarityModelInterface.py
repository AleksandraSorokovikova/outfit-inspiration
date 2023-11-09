from keras.src.preprocessing.image import DirectoryIterator

from config import MODEL_PATH, BATCH_SIZE
from keras.models import load_model
import numpy as np
from keras.applications.resnet50 import preprocess_input


class SimilarityModelInterface:
    def __init__(self):
        self.model = load_model(MODEL_PATH)

    def get_embeddings(self, images_array: np.array) -> np.array:
        processed_images = np.array([preprocess_input(image) for image in images_array])
        embeddings = self.model.predict(processed_images)
        return np.array(embeddings)

    def get_embedding_for_generator(self, images_generator: DirectoryIterator) -> np.array:
        images_generator.reset()
        embeddings = self.model.predict(
            images_generator,
            steps=(len(images_generator.filenames) // BATCH_SIZE) + 1
        )
        return np.array(embeddings)
