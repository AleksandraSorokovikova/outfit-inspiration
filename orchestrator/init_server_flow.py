import os

os.environ["config"] = "prod"

from data.data import get_and_save_files
from model_interface.image_similarity.config import (
    SIMILARITY_MODEL_PATH,
    SIMILARITY_MODEL_NAME,
    CLASSIFICATION_MODEL_PATH,
    CLASSIFICATION_MODEL_NAME,
)
from model_interface.config import class_to_annoy


def init_server():
    get_and_save_files(keys=SIMILARITY_MODEL_NAME, path_to_save=SIMILARITY_MODEL_PATH)
    get_and_save_files(
        keys=CLASSIFICATION_MODEL_NAME, path_to_save=CLASSIFICATION_MODEL_PATH
    )

    for model in class_to_annoy:
        try:
            get_and_save_files(
                keys=class_to_annoy[model]["name"],
                path_to_save=class_to_annoy[model]["path"],
            )
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    init_server()
