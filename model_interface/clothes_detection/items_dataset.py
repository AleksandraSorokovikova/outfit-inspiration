import os

import numpy as np
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision.io import read_image
from PIL.Image import Image as Image_t
from torchvision.transforms import transforms
from torchvision.transforms.functional import InterpolationMode as IM


class ClothesDataset(Dataset):
    def __init__(self, annotations_file: str, img_dir: str) -> None:
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir

    def __len__(self) -> int:
        return len(self.img_labels)

    def resize(
        self,
        img: Image_t,
        target_shape: tuple[int, int],
        pad_val: tuple[int, int, int] = (255, 255, 255),
    ) -> Image:
        original_width, original_height = img.size
        target_width, target_height = target_shape

        aspect_ratio = original_width / original_height
        target_aspect_ratio = target_width / target_height

        if aspect_ratio > target_aspect_ratio:
            # Resize based on the width
            new_width = target_width
            new_height = int(target_width / aspect_ratio)
        else:
            # Resize based on the height
            new_width = int(target_height * aspect_ratio)
            new_height = target_height

        resized_image = img.resize((new_width, new_height))
        padded_image = Image.new("RGB", target_shape, pad_val)

        left = (target_width - new_width) // 2
        top = (target_height - new_height) // 2
        padded_image.paste(resized_image, (left, top))

        return padded_image

    def __getitem__(self, idx: int) -> tuple[Image, tuple[str, str]]:
        raw = self.img_labels.iloc[idx, :]
        img_path = os.path.join(self.img_dir, raw["image_id"])
        image = Image.open(img_path)
        x_min, y_min, x_max, y_max = raw[:4]

        image = image.crop((x_min, y_min, x_max, y_max))

        label = (raw["image_id"], raw["name"])
        image = self.resize(image, (224, 224))

        return image, label
