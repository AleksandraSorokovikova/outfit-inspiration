import os
from typing import Union

import pandas as pd
import torch


class YOLOInterface:
    def __init__(self, weights_path: str, dir_path: str) -> None:
        self._model = torch.hub.load("ultralytics/yolov5", "custom", path=weights_path)
        self._dir_path = dir_path

    def _parse_path(self) -> list[str]:
        all_files = os.listdir(self._dir_path)
        images = [os.path.join(self._dir_path, img.strip()) for img in all_files]

        return images

    def detect(self, images: Union[list[str], None] = None, output_path: Union[str, None] = None) -> pd.DataFrame:
        if images is None:
            images = self._parse_path()

        predictions = self._model(images).pandas().xyxy

        df = pd.DataFrame()

        for target, pic in zip(predictions, images):
            file_name = os.path.basename(pic)
            target["image_id"] = file_name
            df = pd.concat([df, target], ignore_index=True)

        if output_path:
            df.to_csv(output_path)

        return df
