import os

dev_path = "../files/"
prod_path = "../temp_files/"

env = os.getenv("config", "dev")
if env == "dev":
    base_path = dev_path
else:
    base_path = prod_path

DETECTION_CLASSES = {
    0: "Shoes",
    1: "Scarves & Shawls",
    2: "Coats & Jackets",
    3: "Handbags",
    4: "Pants",
    5: "Shirts & Tops",
    6: "Jewelry",
    7: "Sunglasses",
    8: "Dresses",
    9: "Shorts",
    10: "Hats",
    11: "Skirts",
    12: "Watches",
    13: "Socks",
    14: "Jumpsuits & Rompers",
    15: "Rings",
    16: "Belts",
    17: "Stockings",
    18: "Swimwear",
    19: "Gloves & Mittens",
    20: "Neckties",
}
DETECTION_CLASSES_REVERSE = {
    "Shoes": 0,
    "Scarves & Shawls": 1,
    "Coats & Jackets": 2,
    "Handbags": 3,
    "Pants": 4,
    "Shirts & Tops": 5,
    "Jewelry": 6,
    "Sunglasses": 7,
    "Dresses": 8,
    "Shorts": 9,
    "Hats": 10,
    "Skirts": 11,
    "Watches": 12,
    "Socks": 13,
    "Jumpsuits & Rompers": 14,
    "Rings": 15,
    "Belts": 16,
    "Stockings": 17,
    "Swimwear": 18,
    "Gloves & Mittens": 19,
    "Neckties": 20,
}

SIMILARITY_CLASSES = {
    0: 'bag',
    1: 'dress',
    2: 'jumpsuit',
    3: 'outwear',
    4: 'pants',
    5: 'shoes',
    6: 'skirt',
    7: 'top'}

SIMILARITY_CLASSES_REVERSE = {
    "bag": 0,
    "dress": 1,
    "jumpsuit": 2,
    "outwear": 3,
    "pants": 4,
    "shoes": 5,
    "skirt": 6,
    "top": 7
}

SIMILARITY_TO_DETECTION_NAMES = {
    "bag": ["Handbags"],
    "dress": ["Dresses", "Jumpsuits & Rompers"],
    "jumpsuit": ["Jumpsuits & Rompers", "Dresses"],
    "outwear": ["Coats & Jackets", "Shirts & Tops"],
    "pants": ["Pants", "Shorts", "Skirts"],
    "shoes": ["Shoes"],
    "skirt": ["Skirts", "Shorts"],
    "top": ["Shirts & Tops", "Coats & Jackets"]

}

DETECTION_RELEVANT_CLASSES = {i for item in SIMILARITY_TO_DETECTION_NAMES.values() for i in item}

SIMILARITY_TO_DETECTION_INDEXES = {
    SIMILARITY_CLASSES_REVERSE[index_1]: [
        DETECTION_CLASSES_REVERSE[index_2] for index_2 in indices
    ]
    for index_1, indices in SIMILARITY_TO_DETECTION_NAMES.items()
}

garment_to_embedding_path = f"{base_path}garment_to_embedding.json"
garment_to_embedding_name = "garment_to_embedding.json"
garment_to_outfit_path = f"{base_path}garment_to_outfit.json"
garment_to_outfit_name = "garment_to_outfit.json"
outfit_to_garments_path = f"{base_path}outfit_to_garments.json"
outfit_to_garments_name = "outfit_to_garments.json"
class_to_garment_path = f"{base_path}class_to_garment.json"
class_to_garment_name = "class_to_garment.json"

annoy_path = "{0}{1}.ann".format
annoy_name = "{0}.ann".format

class_to_annoy = {
    garment_class: {
        "path": annoy_path(base_path, garment_class),
        "name": annoy_name(garment_class),
    }
    for garment_class in DETECTION_RELEVANT_CLASSES
}
