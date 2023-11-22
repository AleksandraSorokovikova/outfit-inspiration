from annoy import AnnoyIndex
from model_interface.config import class_to_annoy
from tqdm import tqdm
from data.data import upload_file


class AnnoyInterface:

    @staticmethod
    def build_trees_by_dict_and_save(dict_of_classes: dict,
                                     embeddings: dict,
                                     number_of_trees: int = 100,
                                     vector_len: int = 2048,
                                     upload_to_db: bool = True):
        for garment in tqdm(dict_of_classes):
            library = AnnoyIndex(vector_len, 'euclidean')
            for item in dict_of_classes[garment]:
                library.add_item(item, embeddings[item])
            library.build(number_of_trees)
            library.save(class_to_annoy[garment]['path'])
            if upload_to_db:
                upload_file(path=class_to_annoy[garment]['path'], key=class_to_annoy[garment]['name'])
