import os

from model_interface.image_similarity.config import (
    SIMILARITY_MODEL_PATH,
    SIMILARITY_MODEL_NAME,
    CLASSIFICATION_MODEL_PATH,
    CLASSIFICATION_MODEL_NAME,
)

os.environ["config"] = "prod"

from typing import Union

import numpy as np
from PIL import Image
import PIL.Image as Image_t
from data_processor.processor import resize_image
from data.data import get_dict_from_json, get_file, get_and_save_files
from model_interface.image_similarity.SimilarityModelInterface import (
    SimilarityModelInterface,
)
from model_interface.config import (
    SIMILARITY_TO_DETECTION_INDEXES,
    garment_to_outfit_name,
    base_path,
)
from model_interface.clothes_detection.config import img_name
from model_interface.nearest_neighbors.AnnoyInterface import AnnoyInterface


def upload_image(path_to_image: str):
    image = resize_image(path_to_src_image=path_to_image)
    return image


def get_embeddings(image: Image_t):
    image_array = np.array(image)
    image_class = SimilarityModelInterface.get_class([image_array])[0]
    embeddings = SimilarityModelInterface.get_embeddings([image_array])[0]
    detection_classes = SIMILARITY_TO_DETECTION_INDEXES[image_class]
    return detection_classes, embeddings


def select_top_outfits(
    detection_classes: list[int], embeddings: np.ndarray
) -> Union[list[str], None]:
    results = AnnoyInterface.get_predictions_by_model_list(
        detection_classes, embeddings
    )
    if results is None:
        return None
    garment_to_outfit = get_dict_from_json(
        json_filename=garment_to_outfit_name, convert_key_to_digit=True
    )
    outfits = [garment_to_outfit[i] for i in results]
    return outfits


def send_results(source_image: Image_t, outfits: list[str]) -> None:
    found_images = [get_file(f"{img_name}{outfit}") for outfit in outfits]
    found_images = [Image.open(image) for image in found_images]
    import matplotlib.pyplot as plt

    def show_similar_images(source_image: Image_t, found_images: Image_t) -> None:
        plt.figure(figsize=(2, 2))
        plt.axis("off")
        plt.imshow(source_image)
        plt.figure(figsize=(6, 6))
        for i, image in enumerate(found_images[:-1]):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(image)
            plt.axis("off")
            plt.show()

    show_similar_images(source_image, found_images)


def flow(path_to_image: str, dir_path=None) -> list[str]:
    image = upload_image(path_to_image)
    detection_classes, embeddings = get_embeddings(image)
    outfits = select_top_outfits(detection_classes, embeddings)
    outfits = ["pinterest/" + outfit for outfit in outfits]
    get_and_save_files(outfits, dir_path)

    return outfits
