from PIL import Image
import pandas as pd
import os
import numpy as np
from tqdm import tqdm
from datasets import load_dataset, Dataset
from keras.applications.resnet50 import preprocess_input
import functools


def resize_and_save_image(path_to_src_image: str,
                          path_to_target_image: str,
                          new_size: (int, int) = (224, 224)):
    try:
        image = Image.open(path_to_src_image).convert('RGB')
        image_resized = image.resize(new_size)
        image_resized.save(path_to_target_image, 'JPEG', quality=100)
    except Exception as e:
        print(e)


def preprocess_image(example, index, index_to_id):
    image = np.array(example['image'])
    image = np.expand_dims(image, axis=0)
    label = example['label']
    processed_image = preprocess_input(image)

    return {'image': processed_image, 'label': label, 'id': index_to_id[index]}


def create_dataset_with_images(
        images_description_df: pd.DataFrame,
        path_to_folder: str,
        column_with_image_name: str,
        column_with_category_name: str,
        new_size: (int, int) = (224, 224)
) -> Dataset:
    new_folder_name = f'{path_to_folder}_dataset'
    os.makedirs(new_folder_name)
    categories = images_description_df[column_with_category_name].unique().tolist()
    index_to_id = {}
    counter = 0
    for category in tqdm(categories):
        os.makedirs(f'{new_folder_name}/{category}')
        df_category = images_description_df[images_description_df[column_with_category_name] == category]
        for index, row in df_category.iterrows():
            index_to_id[counter] = row[column_with_image_name]
            counter += 1
            src_image_path = f'{path_to_folder}/{row[column_with_image_name]}'
            target_image_path = f'{new_folder_name}/{category}/{row[column_with_image_name]}'
            resize_and_save_image(
                path_to_src_image=src_image_path,
                path_to_target_image=target_image_path,
                new_size=new_size
            )

    dataset = load_dataset(new_folder_name, data_dir="", split='train')
    preprocess_image_partial = functools.partial(preprocess_image, index_to_id=index_to_id)
    processed_dataset = dataset.map(preprocess_image_partial, with_indices=True)
    return processed_dataset
