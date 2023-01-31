"""
Copyright © Aeris1One 2023 (Dandelion)
Copyright © ascpial 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
from __future__ import annotations
from typing import TYPE_CHECKING

import os.path
import requests
import logging

from .config import get_proxy

if TYPE_CHECKING:
    from .extensions import Extension

global_data_structure = [
    "downloaded_data",
    "downloaded_data/sprites",
    "downloaded_data/fonts",
    "tmp",
    "cache",
    "cache/bubbles"
]

global_downloadable_data = {
    "sprites/bubble_back.png": "https://forge.aeris-one.fr/Dandelion/Data/raw/branch/main/bubble_back.png",
    "sprites/bubble_with_frame.png": "https://forge.aeris-one.fr/Dandelion/Data/raw/branch/main/bubble_with_frame.png",
    "fonts/QuickSand-Medium.ttf": "https://forge.aeris-one.fr/Dandelion/Data/raw/branch/main/Quicksand-Medium.ttf"
}

logger = logging.getLogger("libs.data")

def create_data_structure(extension: Extension = None):
    """
    Crée la structure de données.
    
    Si `extension` est spécifié, créé la structure de données pour cette
    extension.
    """
    if extension is None:
        data_structure = global_data_structure
    else:
        data_structure = extension.data_structure

    for folder in data_structure:
        if not os.path.exists(f"/app/data/{folder}"):
            os.mkdir(f"/app/data/{folder}")
            logger.debug(f"Création du dossier /app/data/{folder}")


def clear_tmp():
    """
    Supprime les fichiers temporaires
    """
    for file in os.listdir("/app/data/tmp"):
        os.remove(f"/app/data/tmp/{file}")
        logger.debug(f"Suppression du fichier /app/data/tmp/{file}")


def download_data(extension: Extension = None):
    """
    Télécharge les données supplémentaires.

    Si `extension`  est spécifié, télécharge les données de ce plugin
    spécifiquement.
    """
    if extension is None:
        downloadable_data = global_downloadable_data
    else:
        downloadable_data = extension.downloadable_data

    for file, url in downloadable_data.items():
        with open(f"/app/data/downloaded_data/{file}", "wb") as f:
            f.write(requests.get(url, proxies=get_proxy()).content)
            logger.debug(f"Téléchargement du fichier /app/data/downloaded_data/{file}")
