from annoy import AnnoyIndex
from model_interface.config import class_to_annoy, DETECTION_CLASSES, DETECTION_RELEVANT_CLASSES
from tqdm import tqdm
import numpy as np
from data.data import upload_file


class AnnoyInterface:
    @staticmethod
    def build_trees_by_dict_and_save(
        dict_of_classes: dict,
        embeddings: dict,
        number_of_trees: int = 100,
        vector_len: int = 2048,
        upload_to_db: bool = True,
    ):
        for garment in tqdm(dict_of_classes):
            if garment not in DETECTION_RELEVANT_CLASSES:
                continue
            library = AnnoyIndex(vector_len, "euclidean")
            for item in dict_of_classes[garment]:
                library.add_item(item, embeddings[item])
            library.build(number_of_trees)
            library.save(class_to_annoy[garment]["path"])
            if upload_to_db:
                upload_file(
                    path=class_to_annoy[garment]["path"],
                    key=class_to_annoy[garment]["name"],
                )

    @staticmethod
    def get_predictions_by_model_list(
        list_of_classes: list[int],
        embeddings: np.ndarray,
        top_n: int = 10,
        vector_len: int = 2048,
    ):
        detection_classes_reverse = [DETECTION_CLASSES[i] for i in list_of_classes]
        annoy_models = [i for i in detection_classes_reverse]
        selected_model = None
        lib = AnnoyIndex(vector_len, "euclidean")
        for model in annoy_models:
            try:
                lib.load(class_to_annoy[model]['path'])
                selected_model = model
                break
            except Exception as e:
                continue

        if selected_model is None:
            return None

        results = lib.get_nns_by_vector(embeddings, n=top_n)
        return results
