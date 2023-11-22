base_path = '../files/'

DETECTION_CLASSES = {
    0: 'Shoes',
    1: 'Scarves & Shawls',
    2: 'Coats & Jackets',
    3: 'Handbags',
    4: 'Pants',
    5: 'Shirts & Tops',
    6: 'Jewelry',
    7: 'Sunglasses',
    8: 'Dresses',
    9: 'Shorts',
    10: 'Hats',
    11: 'Skirts',
    12: 'Watches',
    13: 'Socks',
    14: 'Jumpsuits & Rompers',
    15: 'Rings',
    16: 'Belts',
    17: 'Stockings',
    18: 'Swimwear',
    19: 'Gloves & Mittens',
    20: 'Neckties'
}
DETECTION_CLASSES_REVERSE = {
    'Shoes': 0,
    'Scarves & Shawls': 1,
    'Coats & Jackets': 2,
    'Handbags': 3,
    'Pants': 4,
    'Shirts & Tops': 5,
    'Jewelry': 6,
    'Sunglasses': 7,
    'Dresses': 8,
    'Shorts': 9,
    'Hats': 10,
    'Skirts': 11,
    'Watches': 12,
    'Socks': 13,
    'Jumpsuits & Rompers': 14,
    'Rings': 15,
    'Belts': 16,
    'Stockings': 17,
    'Swimwear': 18,
    'Gloves & Mittens': 19,
    'Neckties': 20
}

SIMILARITY_CLASSES = {
    0: 'Blouses_Shirts',
    1: 'Cardigans',
    2: 'Denim',
    3: 'Dresses',
    4: 'Graphic_Tees',
    5: 'Jackets_Coats',
    6: 'Jackets_Vests',
    7: 'Leggings',
    8: 'Pants',
    9: 'Rompers_Jumpsuits',
    10: 'Shirts_Polos',
    11: 'Shorts',
    12: 'Skirts',
    13: 'Suiting',
    14: 'Sweaters',
    15: 'Sweatshirts_Hoodies',
    16: 'Tees_Tanks'
}

SIMILARITY_CLASSES_REVERSE = {
    'Blouses_Shirts': 0,
    'Cardigans': 1,
    'Denim': 2,
    'Dresses': 3,
    'Graphic_Tees': 4,
    'Jackets_Coats': 5,
    'Jackets_Vests': 6,
    'Leggings': 7,
    'Pants': 8,
    'Rompers_Jumpsuits': 9,
    'Shirts_Polos': 10,
    'Shorts': 11,
    'Skirts': 12,
    'Suiting': 13,
    'Sweaters': 14,
    'Sweatshirts_Hoodies': 15,
    'Tees_Tanks': 16
}

SIMILARITY_TO_DETECTION_NAMES = {
    'Blouses_Shirts': ['Shirts & Tops', 'Dresses', 'Jumpsuits & Rompers', 'Coats & Jackets'],
    'Cardigans': ['Coats & Jackets', 'Shirts & Tops'],
    'Denim': ['Pants', 'Shorts', 'Skirts', 'Jumpsuits & Rompers', 'Stockings'],
    'Dresses': ['Dresses', 'Jumpsuits & Rompers', 'Shirts & Tops'],
    'Graphic_Tees': ['Shirts & Tops', 'Dresses', 'Jumpsuits & Rompers', 'Coats & Jackets'],
    'Jackets_Coats': ['Coats & Jackets', 'Shirts & Tops'],
    'Jackets_Vests': ['Shirts & Tops', 'Dresses', 'Coats & Jackets'],
    'Leggings': ['Stockings', 'Pants', 'Jumpsuits & Rompers'],
    'Pants': ['Pants', 'Shorts', 'Skirts', 'Jumpsuits & Rompers', 'Stockings'],
    'Rompers_Jumpsuits': ['Jumpsuits & Rompers', 'Coats & Jackets'],
    'Shirts_Polos': ['Shirts & Tops', 'Dresses', 'Jumpsuits & Rompers', 'Coats & Jackets'],
    'Shorts': ['Shorts', 'Skirts', 'Pants', 'Jumpsuits & Rompers', 'Stockings'],
    'Skirts': ['Skirts', 'Shorts', 'Dresses', 'Pants'],
    'Suiting': ['Coats & Jackets', 'Shirts & Tops', 'Dresses', 'Jumpsuits & Rompers'],
    'Sweaters': ['Shirts & Tops', 'Coats & Jackets', 'Dresses', 'Jumpsuits & Rompers'],
    'Sweatshirts_Hoodies': ['Shirts & Tops', 'Coats & Jackets', 'Dresses'],
    'Tees_Tanks': ['Shirts & Tops', 'Dresses', 'Coats & Jackets', 'Jumpsuits & Rompers']
}

SIMILARITY_TO_DETECTION_INDEXES = {
    SIMILARITY_CLASSES_REVERSE[index_1]: [DETECTION_CLASSES_REVERSE[index_2] for index_2 in indices]
    for index_1, indices in SIMILARITY_TO_DETECTION_NAMES.items()
}

garment_to_embedding_path = f'{base_path}garment_to_embedding.json'
garment_to_embedding_name = 'garment_to_embedding.json'
garment_to_outfit_path = f'{base_path}garment_to_outfit.json'
garment_to_outfit_name = 'garment_to_outfit.json'
outfit_to_garments_path = f'{base_path}outfit_to_garments.json'
outfit_to_garments_name = 'outfit_to_garments.json'
class_to_garment_path = f'{base_path}class_to_garment.json'
class_to_garment_name = 'class_to_garment.json'

annoy_path = '{0}{1}.ann'.format
annoy_name = '{0}.ann'.format

class_to_annoy = {
    garment_class: {'path': annoy_path(base_path, garment_class), 'name': annoy_name(garment_class)}
    for garment_class in DETECTION_CLASSES_REVERSE
}
