from PIL import Image
import pandas as pd
import os
from tqdm import tqdm
from sklearn.model_selection import train_test_split


def resize_and_save_image(path_to_src_image: str,
                          path_to_target_image: str,
                          new_size: (int, int) = (224, 224)):
    try:
        image = Image.open(path_to_src_image).convert('RGB')
        image_resized = image.resize(new_size)
        image_resized.save(path_to_target_image, 'JPEG', quality=100)
    except Exception as e:
        print(e)


def create_images_folder(
        images_description_df: pd.DataFrame,
        path_to_folder: str,
        column_with_image_name: str,
        column_with_category_name: str,
        new_folder_name: str,
        new_size: (int, int) = (224, 224),
        frac: float = 1,
        train_split: float = 0.9,
        validation_split: float = 1
) -> dict[str, dict]:
    def process_df(categories: list[str], df: pd.DataFrame, folder_name: str):
        for category in tqdm(sorted(categories)):
            os.makedirs(f'{folder_name}/{category}')
            df_category = df[df[column_with_category_name] == category]
            for index, row in df_category.iterrows():
                src_image_path = f'{path_to_folder}/{row[column_with_image_name]}'
                target_image_path = f'{folder_name}/{category}/{row[column_with_image_name]}'
                resize_and_save_image(
                    path_to_src_image=src_image_path,
                    path_to_target_image=target_image_path,
                    new_size=new_size
                )

    def index_to_id_fun(path: str):
        counter = 0
        result = {}
        folders = sorted(os.listdir(path))
        for folder in folders:
            if folder == '.DS_Store':
                continue
            for image in sorted(os.listdir(f'{path}/{folder}')):
                if image == '.DS_Store':
                    continue
                result[counter] = image
                counter += 1

        return result

    os.makedirs(new_folder_name)

    categories = images_description_df[column_with_category_name].unique().tolist()
    train, test = train_test_split(images_description_df.sample(frac=frac), train_size=train_split)
    test, validation = train_test_split(test, train_size=validation_split)

    os.makedirs(f'{new_folder_name}/train')
    os.makedirs(f'{new_folder_name}/validation')
    os.makedirs(f'{new_folder_name}/test')

    process_df(categories, train, folder_name=f'{new_folder_name}/train')
    process_df(categories, validation, folder_name=f'{new_folder_name}/validation')
    process_df(categories, test, folder_name=f'{new_folder_name}/test')

    index_to_id = {
        'train': index_to_id_fun(f'{new_folder_name}/train'),
        'validation': index_to_id_fun(f'{new_folder_name}/validation'),
        'test': index_to_id_fun(f'{new_folder_name}/test')
    }

    return index_to_id
