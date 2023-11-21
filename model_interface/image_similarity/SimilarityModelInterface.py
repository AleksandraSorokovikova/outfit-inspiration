from keras import Model

from model_interface.image_similarity.config import MODEL_PATH, BATCH_SIZE, IMAGE_SIZE
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
import numpy as np
from keras.applications.resnet50 import preprocess_input


class SimilarityModelInterface:
    def __init__(self):
        self.classification_model = load_model(MODEL_PATH, compile=False)
        self.similarity_model = Model(
            self.classification_model.input, self.classification_model.layers[-2].output
        )

    def get_embeddings(self, images_array: np.array) -> np.array:
        processed_images = np.array([preprocess_input(image) for image in images_array])
        embeddings = self.similarity_model.predict(processed_images)
        return np.array(embeddings)

    def get_embedding_from_generator(
        self, path_to_directory: str, include_filenames: bool = False
    ) -> np.array:
        image_generator = ImageDataGenerator(preprocessing_function=preprocess_input)
        dataset = image_generator.flow_from_directory(
            path_to_directory,
            class_mode="categorical",
            target_size=IMAGE_SIZE,
            color_mode="rgb",
            shuffle=False,
            batch_size=BATCH_SIZE,
        )
        dataset.reset()
        embeddings = self.similarity_model.predict(
            dataset, steps=(len(dataset.filenames) // BATCH_SIZE) + 1
        )
        result = np.array(embeddings)
        if include_filenames:
            result = [(dataset.filenames[i], vector) for i, vector in enumerate(result)]
        return result

    def get_class(self, images_array: np.array) -> np.array:
        processed_images = np.array([preprocess_input(image) for image in images_array])
        predictions = self.classification_model.predict(processed_images)
        classes = np.argmax(predictions, axis=1)
        return classes
