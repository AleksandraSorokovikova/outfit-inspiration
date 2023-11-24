from collections import defaultdict

import numpy as np
import json

from model_interface.clothes_detection.yolo_interface import YOLOInterface
from model_interface.clothes_detection.items_dataset import ClothesDataset
from model_interface.image_similarity.SimilarityModelInterface import SimilarityModelInterface
from model_interface.clothes_detection.config import (
    model_path,
    model_name,
    img_dir,
    base_path,
    img_name,
    annotations_file,
    segments_file_path,
    segments_file_name,
)
from data.data import upload_file, get_and_save_files, get_and_save_folder
from model_interface.image_similarity.config import SIMILARITY_MODEL_PATH, SIMILARITY_MODEL_NAME
from model_interface.config import *
from model_interface.nearest_neighbors.AnnoyInterface import AnnoyInterface


def detect_clothes() -> None:
    get_and_save_files(path_to_save=model_path, keys=model_name)
    get_and_save_folder(path_to_folder=base_path, key_folder_name=img_name)
    model = YOLOInterface(model_path, img_dir)
    results = model.detect(None, annotations_file)
    results.to_csv(segments_file_path, index=False)
    upload_file(path=segments_file_path, key=segments_file_name)


def create_embeddings() -> None:
    def save_and_upload_json(data: dict, path: str, name: str) -> None:
        with open(path, "w") as write_file:
            json.dump(data, write_file)
        upload_file(path, name)

    get_and_save_files(keys=SIMILARITY_MODEL_NAME, path_to_save=SIMILARITY_MODEL_PATH)

    dataset = ClothesDataset(segments_file_path, img_dir)

    batch_size = 128
    garment_to_outfit = {}
    class_to_garments = defaultdict(list)
    outfit_to_garments = defaultdict(list)
    garment_to_embedding = {}

    for batch in np.array_split(
        np.arange(0, len(dataset)), len(dataset) // batch_size + 1
    ):
        images = []

        for i in batch:
            index = int(i)
            image, label = dataset[index]
            outfit, garment_class = label
            images.append(np.array(image))
            garment_to_outfit[index] = outfit
            class_to_garments[garment_class].append(index)
            outfit_to_garments[outfit].append(index)

        embeddings = SimilarityModelInterface.get_embeddings(images)
        for i, index in enumerate(batch):
            garment_to_embedding[int(index)] = embeddings[i].tolist()

    save_and_upload_json(
        garment_to_outfit, garment_to_outfit_path, garment_to_outfit_name
    )
    save_and_upload_json(
        dict(class_to_garments), class_to_garment_path, class_to_garment_name
    )
    save_and_upload_json(
        dict(outfit_to_garments), outfit_to_garments_path, outfit_to_garments_name
    )
    save_and_upload_json(
        garment_to_embedding, garment_to_embedding_path, garment_to_embedding_name
    )

    AnnoyInterface.build_trees_by_dict_and_save(
        dict_of_classes=class_to_garments, embeddings=garment_to_embedding
    )


def flow() -> None:
    detect_clothes()
    create_embeddings()


if __name__ == "__main__":
    flow()
