"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""

# Import modules
import random

import peewee
from PIL import Image

from lib.database import Avatar

# Fonction user_has_avatar
# ---
# Entrée :
# - userid Discord (int)
# Sortie :
# - bool
# ---
# Vérifie si l'utilisateur spécifié a un avatar
def user_has_avatar(userid: int) -> bool:
    try:
        Avatar().get(Avatar.user_id == userid)
        return True
    except peewee.DoesNotExist:
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
    # Supprimer l'avatar de l'utilisateur dans la base de données
    Avatar().delete().where(Avatar.user_id == userid).execute()


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
# - None
# ---
# Créer un avatar pour l'utilisateur spécifié
def create_avatar(userid: int,
                  skin_color: int,
                  clothes: list,
                  hair_type: str,
                  accessories: list,
                  lipstick: bool,
                  blush: bool
                  ):
    # Ouvrir la bonne peau
    avatar = Image.open(f"data/sprites/characters/char{skin_color}.png")

    # Ajouter des yeux d'une couleur aléatoire
    eyes_grid = Image.open("data/sprites/eyes/eyes.png")
    eyes_colors = eyes_grid.width // 256
    eyes_color = random.randint(0, eyes_colors - 1)
    eyes_grid = eyes_grid.crop((eyes_color * 256, 0, (eyes_color + 1) * 256, eyes_grid.height))
    avatar.paste(eyes_grid, (0, 0), eyes_grid)

    # Ajouter un rouge à lèvre si besoin
    if lipstick:
        lipstick_grid = Image.open("data/sprites/eyes/lipstick.png")
        lipstick_colors = lipstick_grid.width // 256
        lipstick_color = random.randint(0, lipstick_colors - 1)
        lipstick_grid = lipstick_grid.crop((lipstick_color * 256, 0, (lipstick_color + 1) * 256, lipstick_grid.height))
        avatar.paste(lipstick_grid, (0, 0), lipstick_grid)

    # Ajouter un blush si besoin
    if blush:
        blush_grid = Image.open("data/sprites/eyes/blush.png")
        blush_colors = blush_grid.width // 256
        blush_color = random.randint(0, blush_colors - 1)
        blush_grid = blush_grid.crop((blush_color * 256, 0, (blush_color + 1) * 256, blush_grid.height))
        avatar.paste(blush_grid, (0, 0), blush_grid)

    # Appliquer les vêtements
    for cloth in clothes:
        cloth_grid = Image.open(f"data/sprites/clothes/{cloth}.png")
        cloth_colors = cloth_grid.width // 256
        cloth_color = random.randint(0, cloth_colors - 1)
        cloth_grid = cloth_grid.crop((cloth_color * 256, 0, (cloth_color + 1) * 256, cloth_grid.height))
        avatar.paste(cloth_grid, (0, 0), cloth_grid)

    # Ajouter les cheveux
    if hair_type is not None:
        hair_grid = Image.open(f"data/sprites/hair/{hair_type}.png")
        hair_colors = hair_grid.width // 256
        hair_color = random.randint(0, hair_colors - 1)
        hair_grid = hair_grid.crop((hair_color * 256, 0, (hair_color + 1) * 256, hair_grid.height))
        avatar.paste(hair_grid, (0, 0), hair_grid)

    # Ajouter les accessoires
    for accessory in accessories:
        accessory_grid = Image.open(f"data/sprites/acc/{accessory}.png")
        accessory_colors = accessory_grid.width // 256
        accessory_color = random.randint(0, accessory_colors - 1)
        accessory_grid = accessory_grid.crop(
            (accessory_color * 256, 0, (accessory_color + 1) * 256, accessory_grid.height))
        avatar.paste(accessory_grid, (0, 0), accessory_grid)

    # Enregistrer l'avatar dans la base de données
    avatar = Avatar(user_id=userid, avatar=avatar.tobytes())
    avatar.save()


# Fonction retrieve_avatar_sprite
# ---
# Entrée :
# - userid Discord          (int)
# - x position              (int)
# - y position              (int)
# Sortie :
# - sprite de l'avatar      (PIL.Image)
# ---
# Récupérer le carré à la position x, y de l'avatar de l'utilisateur
def retrieve_avatar_sprite(userid: int):
    # Récupérer l'avatar de l'utilisateur dans la base de données
    print(f'User {userid} has avatar: {user_has_avatar(userid)}')
    avatar = Avatar().get(Avatar.user_id == userid).avatar
    avatar = Image.frombytes("RGBA", (256, 1568), avatar)

    # Retourner le sprite
    return avatar
