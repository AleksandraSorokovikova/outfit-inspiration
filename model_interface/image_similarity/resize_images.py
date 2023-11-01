from PIL import Image
from tqdm.notebook import tqdm
import os


def resize_images(path_to_src_folder: str,
                  path_to_target_folder: str,
                  new_size: (int, int) = (224, 224)):
    dirs = os.listdir(path_to_src_folder)
    for item in tqdm(dirs):
        try:
            image = Image.open(path_to_src_folder + item)
            image_resized = image.resize(new_size)
            image_resized.save(path_to_target_folder + item, 'JPEG', quality=100)
        except:
            pass
