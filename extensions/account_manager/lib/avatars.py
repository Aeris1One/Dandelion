"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

import logging
# Import modules
import random

import peewee
from PIL import Image

from lib.database import open_db, close_db
from .database import Avatar

logger = logging.getLogger("account_manager.libs.avatars")


# Fonction user_has_avatar
# ---
# Entrée :
# - userid Discord (int)
# Sortie :
# - bool
# ---
# Vérifie si l'utilisateur spécifié a un avatar
def user_has_avatar(userid: int) -> bool:
    logger.debug(f"Vérification de l'existence de l'avatar de l'utilisateur {userid}")
    try:
        open_db()
        Avatar().get(Avatar.user_id == userid)
        close_db()
        logger.debug(f"L'utilisateur {userid} a un avatar")
        return True
    except peewee.DoesNotExist:
        logger.debug(f"L'utilisateur {userid} n'a pas d'avatar")
        return False


# Fonction delete_avatar
# ---
# Entrée :
# - userid Discord (int)
# Sortie :
# - None
# ---
# Supprime l'avatar de l'utilisateur spécifié
def delete_avatar(userid: int):
    logger.debug(f"Suppression de l'avatar de l'utilisateur {userid}")

    # Supprimer l'avatar de l'utilisateur dans la base de données
    Avatar().delete().where(Avatar.user_id == userid).execute()
    logger.debug(f"L'avatar de l'utilisateur {userid} a été supprimé")


# Fonction create_avatar
# ---
# Entrée :
# - userid Discord          (int)
# - couleur de peau         (int)
# - liste de vêtements      (list)
# - type de cheveux         (str)
# - liste d'accessoires     (list)
# - rouge à lèvre           (bool)
# - blush                   (bool)
# Sortie :
# - avatar                  (PIL.Image)
# ---
# Créer un avatar pour l'utilisateur spécifié
def create_avatar(skin_color: int,
                  clothes: list,
                  hair_type: str,
                  accessories: list,
                  lipstick: bool,
                  blush: bool
                  ):
    # Logs
    logger.debug(f"Création d'un avatar pour l'utilisateur")

    # Ouvrir la bonne peau
    avatar = Image.open(f"data/sprites/characters/char{skin_color}.png")
    logger.debug("Peau chargée")

    # Ajouter des yeux d'une couleur aléatoire
    eyes_grid = Image.open("data/sprites/eyes/eyes.png")
    eyes_colors = eyes_grid.width // 256
    eyes_color = random.randint(0, eyes_colors - 1)
    eyes_grid = eyes_grid.crop((eyes_color * 256, 0, (eyes_color + 1) * 256, eyes_grid.height))
    avatar.paste(eyes_grid, (0, 0), eyes_grid)
    logger.debug("Yeux ajoutés")

    # Ajouter un rouge à lèvre si besoin
    if lipstick:
        lipstick_grid = Image.open("data/sprites/eyes/lipstick.png")
        lipstick_colors = lipstick_grid.width // 256
        lipstick_color = random.randint(0, lipstick_colors - 1)
        lipstick_grid = lipstick_grid.crop((lipstick_color * 256, 0, (lipstick_color + 1) * 256, lipstick_grid.height))
        avatar.paste(lipstick_grid, (0, 0), lipstick_grid)
        logger.debug("Rouge à lèvre ajouté")

    # Ajouter un blush si besoin
    if blush:
        blush_grid = Image.open("data/sprites/eyes/blush.png")
        blush_colors = blush_grid.width // 256
        blush_color = random.randint(0, blush_colors - 1)
        blush_grid = blush_grid.crop((blush_color * 256, 0, (blush_color + 1) * 256, blush_grid.height))
        avatar.paste(blush_grid, (0, 0), blush_grid)
        logger.debug("Blush ajouté")

    # Appliquer les vêtements
    for cloth in clothes:
        cloth_grid = Image.open(f"data/sprites/clothes/{cloth}.png")
        cloth_colors = cloth_grid.width // 256
        cloth_color = random.randint(0, cloth_colors - 1)
        cloth_grid = cloth_grid.crop((cloth_color * 256, 0, (cloth_color + 1) * 256, cloth_grid.height))
        avatar.paste(cloth_grid, (0, 0), cloth_grid)
        logger.debug(f"Vêtement {cloth} ajouté")

    # Ajouter les cheveux
    if hair_type is not None:
        hair_grid = Image.open(f"data/sprites/hair/{hair_type}.png")
        hair_colors = hair_grid.width // 256
        hair_color = random.randint(0, hair_colors - 1)
        hair_grid = hair_grid.crop((hair_color * 256, 0, (hair_color + 1) * 256, hair_grid.height))
        avatar.paste(hair_grid, (0, 0), hair_grid)
        logger.debug(f"Cheveux {hair_type} ajoutés")

    # Ajouter les accessoires
    for accessory in accessories:
        accessory_grid = Image.open(f"data/sprites/acc/{accessory}.png")
        accessory_colors = accessory_grid.width // 256
        accessory_color = random.randint(0, accessory_colors - 1)
        accessory_grid = accessory_grid.crop(
            (accessory_color * 256, 0, (accessory_color + 1) * 256, accessory_grid.height))
        avatar.paste(accessory_grid, (0, 0), accessory_grid)
        logger.debug(f"Accessoire {accessory} ajouté")

    # Renvoyer l'avatar
    return avatar


# Fonction save_avatar
# ---
# Entrée :
# - userid Discord          (int)
# - avatar      (PIL.Image)
# Sortie :
# - None
# ---
# Enregistrer l'avatar de l'utilisateur dans la base de données
def save_avatar(userid: int, avatar: Image):
    # Logs
    logger.debug(f"Enregistrement de l'avatar de l'utilisateur {userid} dans la base de données")

    # Enregistrer l'avatar de l'utilisateur dans la base de données
    open_db()
    avatar = Avatar(user_id=userid, avatar=avatar.tobytes())
    avatar.save()
    close_db()


# Fonction retrieve_avatar
# ---
# Entrée :
# - userid Discord          (int)
# Sortie :
# - avatar      (PIL.Image)
# ---
# Récupérer l'avatar de l'utilisateur depuis la base de données
def retrieve_avatar(userid: int):
    # Logs
    logger.debug(f"Récupération de l'avatar de l'utilisateur {userid} depuis la base de données")

    # Récupérer l'avatar de l'utilisateur dans la base de données
    open_db()
    avatar = Avatar().get(Avatar.user_id == userid).avatar
    avatar = Image.frombytes("RGBA", (256, 1568), avatar)
    close_db()

    # Retourner le sprite
    return avatar
