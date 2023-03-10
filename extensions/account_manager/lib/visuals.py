"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging
import os
import random

import PIL
import discord
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import extensions.account_manager.lib.avatars as avatars

logger = logging.getLogger("account_manager.lib.visuals")

emoticons_coord = {
    "unimpressed": (0, 0),
    "angry": (1, 0),
    "surprised": (2, 0),
    "relaxed": (3, 0),
    "cool": (4, 0),
    "happy": (0, 1),
    "tired": (1, 1),
    "flirting": (2, 1),
    "love": (3, 1),
    "upset": (4, 1),
    "embarrassed": (0, 2),
    "amused": (1, 2),
    "annoyed": (2, 2),
    "crying": (3, 2),
    "pleased": (4, 2),
}


def generate_bubble(emoticon: str, text: str, cache: bool = True) -> discord.File:
    """
    Génère une bulle de dialogue avec l'émoticône spécifié et le texte spécifié

    :param emoticon:
    :param text:
    :param cache:
    :return:
    """
    logger.debug(f"Génération d'une bulle avec l'icone '{emoticon}' et le texte '{text}'")
    # Si le fichier existe déjà en cache, on le renvoie
    # On vérifie que le texte est toujours le même
    if cache and os.path.exists(f"/app/data/cache/bubbles/{hash(emoticon)}-{hash(text)}.gif"):
        logger.debug("La bulle est déjà en cache, renvoi du fichier")
        output = discord.File(f"/app/data/cache/bubbles/{hash(emoticon)}-{hash(text)}.gif")

    # Sinon, on le génère
    else:
        # Ouvrir l'arrière-plan
        bubble_back = Image.open("/app/data/downloaded_data/sprites/bubble_back.png")
        bubble_back = bubble_back.resize((512, 128), Image.NEAREST)

        # Ouvrir l'emoticone
        emoticon_sprite = retrieve_emoticon_sprite(emoticons_coord[emoticon])
        emoticon_sprite = emoticon_sprite.resize((96, 96), Image.NEAREST)

        # Ouvrir la police d'écriture
        font = ImageFont.truetype("/app/data/downloaded_data/fonts/QuickSand-Medium.ttf", 18)

        # Générer les bulles
        bubbles = []
        for i in np.arange(0, 2 * np.pi, np.pi / 12):
            # On récupère l'arrière-plan
            bubble = bubble_back.copy()
            # On colle l'émoticone au bon endroit (on utilise le cosinus pour l'animation de vaguelette)
            bubble.paste(emoticon_sprite, (12, 16 + round(6 * np.cos(i))), emoticon_sprite)
            # On écrit le texte
            bubble_draw = ImageDraw.Draw(bubble)
            # On décale le texte de 12 pixels (bord - emoticone), + 96 pixels (emoticone) et + 10 pixels (espace
            # entre l'emoticone et le texte) soit 118 pixels On centre verticalement avec anchor="lm" (l middle)
            bubble_draw.multiline_text((118, 64), text, font=font, fill=(0, 0, 0), align="center", anchor="lm")
            bubbles.append(bubble)

        # Sauvegarder la bulle
        # Dans le cache si c'est demandé
        if cache:
            logger.debug("Sauvegarde de la bulle dans le cache")
            bubbles[0].save(f"/app/data/cache/bubbles/{hash(emoticon)}-{hash(text)}.gif",
                            save_all=True, append_images=bubbles[1:],
                            optimize=False, duration=100, loop=0)
            logger.debug("Sauvegarde terminée, renvoi du fichier")
            output = discord.File(f"/app/data/cache/bubbles/{hash(emoticon)}-{hash(text)}.gif")

        # Sinon dans le dossier temporaire et on le supprime après
        else:
            # Générer un ID aléatoire pour éviter les conflits de fichiers
            random_tmp = random.randint(0, 1024)
            logger.debug(f"Sauvegarde de la bulle dans le dossier temporaire avec l'ID {random_tmp}")
            bubbles[0].save(f'/app/data/tmp/bubbles-{hash(emoticon)}-{hash(text)}-{random_tmp}.gif',
                            save_all=True, append_images=bubbles[1:],
                            optimize=False, duration=100, loop=0)
            logger.debug("Sauvegarde terminée, renvoi du fichier")
            output = discord.File(f'/app/data/tmp/bubbles-{hash(emoticon)}-{hash(text)}-{random_tmp}.gif')
            logger.debug("Suppression du fichier temporaire")
            os.remove(f'/app/data/tmp/bubbles-{hash(emoticon)}-{hash(text)}-{random_tmp}.gif')
            logger.debug("Suppression terminée")

    # Renvoyer le fichier
    return output


def generate_bubble_with_avatar(emoticon: str, text: str, *, image: PIL.Image = None,
                                userid: int = None) -> discord.File:
    """
    Génère une bulle de dialogue avec l'émoticône spécifié, le texte spécifié et l'avatar de l'utilisateur spécifié
    en animation de marche

    :param image:
    :param emoticon:
    :param text:
    :param userid:
    :return:
    """
    logger.debug(f"Génération d'une bulle avec l'icone '{emoticon}', le texte '{text}' et l'avatar de l'utilisateur")

    # Ouvrir l'arrière-plan
    bubble_back = Image.open(f"/app/data/downloaded_data/sprites/bubble_with_frame.png")
    bubble_back = bubble_back.resize((512, 576), Image.NEAREST)

    # Ouvrir l'emoticone
    emoticon_sprite = retrieve_emoticon_sprite(emoticons_coord[emoticon])
    emoticon_sprite = emoticon_sprite.resize((96, 96), Image.NEAREST)

    # Ouvrir la police
    font = ImageFont.truetype("/app/data/downloaded_data/fonts/QuickSand-Medium.ttf", 18)

    # Ouvrir l'avatar
    if image is not None:
        avatar = image
    elif userid is not None:
        logger.debug(f"Récupération de l'avatar de l'utilisateur {userid} depuis la base de données")
        avatar = avatars.retrieve_avatar(userid)
    else:
        logging.error("generate_bubble_with_avatar: ni image ni userid n'a été spécifié")

    # Générer les bulles
    bubbles = []
    for i in np.arange(0, 2 * np.pi, np.pi / 8):
        # On récupère l'arrière-plan
        bubble = bubble_back.copy()

        # On récupère le sprite de l'avatar de l'utilisateur
        x = round(i / (np.pi / 8)) % 8
        char = avatar.copy()
        char = char.crop((x * 32, 0, (x + 1) * 32, 32))
        char = char.resize((384, 384), Image.NEAREST)

        # On colle l'émoticône au bon endroit (on utilise le cosinus pour l'animation de vaguelette)
        bubble.paste(emoticon_sprite, (12, 16 + round(6 * np.cos(i))), emoticon_sprite)

        # On colle l'avatar au bon endroit
        bubble.paste(char, (64, 130), char)

        # On écrit le texte
        bubble_draw = ImageDraw.Draw(bubble)
        bubble_draw.multiline_text((118, 64), text, font=font, fill=(0, 0, 0), align="center", anchor="lm")
        bubbles.append(bubble)

    # Sauvegarder la bulle
    # On ne cache pas les bulles avec avatar, parce qu'elles sont très souvent uniques et les
    # stocker prendrait de la place
    random_tmp = random.randint(0, 1024)
    logger.debug(f"Sauvegarde de la bulle dans le dossier temporaire avec l'ID {random_tmp}")
    bubbles[0].save(f'/app/data/tmp/bubbles-{hash(emoticon)}-{hash(text)}-{random_tmp}.gif',
                    save_all=True, append_images=bubbles[1:],
                    optimize=False, duration=130, loop=0)
    logger.debug("Sauvegarde terminée, renvoi du fichier")
    output = discord.File(f'/app/data/tmp/bubbles-{hash(emoticon)}-{hash(text)}-{random_tmp}.gif')
    logger.debug("Suppression du fichier temporaire")
    os.remove(f'/app/data/tmp/bubbles-{hash(emoticon)}-{hash(text)}-{random_tmp}.gif')
    logger.debug("Suppression terminée")

    # Renvoyer le fichier
    return output


def retrieve_emoticon_sprite(coords: tuple):
    """
    Récupère le sprite d'une émoticône à partir de ses coordonnées dans la grille

    :param coords: tuple (x, y)
    :return: Image
    """

    # Logs
    logger.debug(f"Récupération du sprite de l'emoticône aux coordonnées {coords}")

    # Récupérer les coordonnées
    x, y = coords

    # Ouvrir la grille
    emoticon = Image.open(f"data/sprites/emoticons.png")

    # Couper la bonne case
    emoticon = emoticon.crop((x * 16, y * 16, (x + 1) * 16, (y + 1) * 16))

    # Renvoyer la case coupée
    return emoticon
