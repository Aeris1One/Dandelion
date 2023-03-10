"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging
import os

import discord

import extensions.account_manager.lib.avatars as avatars
import extensions.account_manager.lib.visuals as visuals
import extensions.account_manager.main_menu.confirm as confirm

logger = logging.getLogger("account_manager.misc")


async def timeout_message(interaction: discord.Interaction):
    await interaction.edit_original_response(attachments=[visuals.generate_bubble("embarrassed",
                                                                                  "Tu as pris trop de temps pour "
                                                                                  "répondre !\nExécute la commande "
                                                                                  "à nouveau\n pour recommencer.")],
                                             view=None
                                             )


async def do_nothing(interaction: discord.Interaction):
    await interaction.response.edit_message(attachments=[visuals.generate_bubble("angry",
                                                                                 "Eh ! Si tu ne veux rien faire, "
                                                                                 "tu n'as qu'à\nne pas utiliser la "
                                                                                 "commande !")],
                                            view=None
                                            )


async def delete_avatar(interaction: discord.Interaction):
    action, interaction = await confirm.confirm(interaction)
    if action == "timeout":
        await timeout_message(interaction)
    elif not bool(action):
        await interaction.response.edit_message(attachments=[visuals.generate_bubble("happy",
                                                                                     "Tu as annulé la suppression "
                                                                                     "de ton avatar !")],
                                                view=None
                                                )
    else:
        avatars.delete_avatar(interaction.user.id)
        await interaction.response.edit_message(attachments=[visuals.generate_bubble("happy",
                                                                                     "Ton avatar a bien été "
                                                                                     "supprimé !")],
                                                view=None
                                                )


async def error_message(interaction: discord.Interaction):
    await interaction.response.edit_message(attachments=[visuals.generate_bubble("angry",
                                                                                 "Une erreur est survenue !\n"
                                                                                 "Veuillez contacter le "
                                                                                 "support si cela se\n"
                                                                                 "produit à nouveau !")],
                                            view=None
                                            )


def check_sprites():
    """
    Vérifie si les sprites sont présents dans le dossier

    :return: True si les sprites sont présents, False sinon
    """
    if os.path.exists("/app/data/sprites"):
        # TODO : vérifier que les fichiers sont bien là !
        return True
    return False


def correct_sprites_filenames():
    """
    Corrige les sprites
    """
    for directory in os.listdir("/app/data/sprites"):
        if os.path.isdir(f"/app/data/sprites/{directory}"):
            for file in os.listdir(f"/app/data/sprites/{directory}"):
                if " ." in file:
                    os.rename(f"/app/data/sprites/{directory}/{file}",
                              f"/app/data/sprites/{directory}/{file.replace(' .', '.')}")
                    logger.debug(
                        f"Renommage du fichier /app/data/sprites/{directory}/{file} en /app/data/sprites/{directory}/{file.replace(' .', '.')}")

    # Renommer data/sprites/eyes/blush_all.png en blush.png
    if os.path.exists("/app/data/sprites/eyes/blush_all.png"):
        os.rename(
            "/app/data/sprites/eyes/blush_all.png",
            "/app/data/sprites/eyes/blush.png"
        )
        logger.debug("Renommage du fichier /app/data/sprites/eyes/blush_all.png en /app/data/sprites/eyes/blush.png")
