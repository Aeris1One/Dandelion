"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import os.path
import requests

data_structure = [
    "downloaded_data",
    "downloaded_data/sprites",
    "downloaded_data/fonts",
    "tmp",
    "cache",
    "cache/bubbles"
]

downloadable_data = {
    "sprites/bubble_back.png": "https://forge.aeris-one.fr/Dandelion/Data/raw/branch/main/bubble_back.png",
    "sprites/bubble_with_frame.png": "https://forge.aeris-one.fr/Dandelion/Data/raw/branch/main/bubble_with_frame.png",
    "fonts/QuickSand-Medium.ttf": "https://forge.aeris-one.fr/Dandelion/Data/raw/branch/main/Quicksand-Medium.ttf"
}


def check_sprites():
    """
    Vérifie si les sprites sont présents dans le dossier

    :return: True si les sprites sont présents, False sinon
    """
    if os.path.exists("/app/data/sprites"):
        # TODO : vérifier que les fichiers sont bien là !
        return True
    return False


def create_data_structure():
    """
    Crée la structure de données
    """
    for folder in data_structure:
        if not os.path.exists(f"/app/data/{folder}"):
            os.mkdir(f"/app/data/{folder}")


def clear_tmp():
    """
    Supprime les fichiers temporaires
    """
    for file in os.listdir("/app/data/tmp"):
        os.remove(f"/app/data/tmp/{file}")


def download_data():
    """
    Télécharge les données supplémentaires
    """
    for file, url in downloadable_data.items():
        with open(f"/app/data/downloaded_data/{file}", "wb") as f:
            f.write(requests.get(url).content)


def correct_sprites_filenames():
    """
    Corrige les sprites
    """
    for directory in os.listdir("/app/data/sprites"):
        if os.path.isdir(f"/app/data/sprites/{directory}"):
            for file in os.listdir(f"/app/data/sprites/{directory}"):
                if " ." in file:
                    os.rename(f"/app/data/sprites/{directory}/{file}", f"/app/data/sprites/{directory}/{file.replace(' .', '.')}")

    # Renommer data/sprites/eyes/blush_all.png en blush.png
    if os.path.exists("/app/data/sprites/eyes/blush_all.png"):
        os.rename(
            "/app/data/sprites/eyes/blush_all.png",
            "/app/data/sprites/eyes/blush.png"
        )
