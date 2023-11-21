names = {
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
names_rev = {
    names[ind]: ind for ind in names
}

MODEL_CLASSES = {
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

MODEL_CLASSES_rev = {
    MODEL_CLASSES[ind]: ind for ind in MODEL_CLASSES
}

result = {'Blouses_Shirts': ['Shirts & Tops', 'Dresses', 'Jumpsuits & Rompers', 'Coats & Jackets'],
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
          'Suiting': ['Coats & Jackets',
                      'Shirts & Tops',
                      'Dresses',
                      'Jumpsuits & Rompers'],
          'Sweaters': ['Shirts & Tops', 'Coats & Jackets',
                       'Dresses',
                       'Jumpsuits & Rompers'],
          'Sweatshirts_Hoodies': ['Shirts & Tops', 'Coats & Jackets', 'Dresses'],
          'Tees_Tanks': ['Shirts & Tops', 'Dresses', 'Coats & Jackets', 'Jumpsuits & Rompers']}

result_rev = {
    MODEL_CLASSES_rev[index_1]: [names_rev[index_2] for index_2 in indices]
    for index_1, indices in result.items()
}
