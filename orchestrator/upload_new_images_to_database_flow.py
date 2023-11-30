# Пока что тут иммитация airflow dag, позже превратится в настоящий dag

import os
import pandas as pd
from data.data import upload_file, upload_files
from data_processor.processor import create_images_folder
import json
from model_interface.image_similarity.config import (
    BASE_PATH,
    TRAIN_SPLIT,
    VALIDATION_SPLIT,
    ORIG_INPUT_DATASET,
    IMAGES_DESCRIPTION_PATH,
)


def load_new_images() -> tuple[str, str]:
    images_folder = ORIG_INPUT_DATASET
    images_description = IMAGES_DESCRIPTION_PATH
    return images_folder, images_description


def preprocess_images(
    path_to_images_folder: str, path_to_images_description: str
) -> tuple[str, dict[str, dict]]:
    folder_dataset = BASE_PATH
    images_description = pd.read_csv(path_to_images_description)
    index_to_id = create_images_folder(
        images_description_df=images_description,
        path_to_folder=path_to_images_folder,
        column_with_image_name="file_name",
        column_with_category_name="category",
        new_folder_name=folder_dataset,
        train_split=TRAIN_SPLIT,
        validation_split=VALIDATION_SPLIT,
    )
    return folder_dataset, index_to_id


def upload_preprocessed_images_to_database(
    path_to_processed_images: str, index_to_id: dict[str, dict]
) -> None:
    all_files = []
    for address, dirs, files in os.walk(path_to_processed_images):
        for name in files:
            file = os.path.join(address, name)
            if ".DS_Store" not in file:
                all_files.append(file)
    print("Total number of files:", len(all_files))
    index_to_id_file = "images_embeddings_dataset_index_to_id.json"
    with open(index_to_id_file, "w") as json_file:
        json.dump(index_to_id, json_file)

    upload_file(index_to_id_file, index_to_id_file)
    upload_files(all_files)
    print("Success!")


def flow():
    images_folder, images_description = load_new_images()
    folder_dataset, index_to_id = preprocess_images(images_folder, images_description)
    upload_preprocessed_images_to_database(folder_dataset, index_to_id)


if __name__ == "__main__":
    flow()
