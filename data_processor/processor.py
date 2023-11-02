from PIL import Image
import pandas as pd
import os
from tqdm import tqdm
from datasets import load_dataset, Dataset


def resize_and_save_image(path_to_src_image: str,
                          path_to_target_image: str,
                          new_size: (int, int) = (224, 224)):
    try:
        image = Image.open(path_to_src_image)
        image_resized = image.resize(new_size)
        image_resized.save(path_to_target_image, 'JPEG', quality=100)
    except Exception as e:
        print(e)


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
    for category in tqdm(categories):
        os.makedirs(f'{new_folder_name}/{category}')
        df_category = images_description_df[images_description_df[column_with_category_name] == category]
        for index, row in df_category.iterrows():
            src_image_path = f'{path_to_folder}/{row[column_with_image_name]}'
            target_image_path = f'{new_folder_name}/{category}/{row[column_with_image_name]}'
            resize_and_save_image(
                path_to_src_image=src_image_path,
                path_to_target_image=target_image_path,
                new_size=new_size
            )

    dataset = load_dataset(new_folder_name, data_dir="", split='train')
    return dataset
