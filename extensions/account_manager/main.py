"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging

import discord

from lib.bot import DandelionClient
from . import misc
from .avatar_creation import main as avatar_creation
from .lib import database
from .main_menu import main as main_menu

logger = logging.getLogger('account_manager')


@discord.app_commands.command(
    name="avatar",
    description="Gère ton avatar"
)
async def avatar(interaction: discord.Interaction) -> None:
    action, interaction = await main_menu.menu(interaction)
    if action == 'create_avatar':
        await avatar_creation.init_avatar_creation(interaction)
    elif action == 'delete_avatar':
        await misc.delete_avatar(interaction)
    elif action == 'timeout':
        await misc.timeout_message(interaction)
    elif action == 'nothing':
        await misc.do_nothing(interaction)
    else:
        await misc.error_message(interaction)


def main(client: DandelionClient):
    if not misc.check_sprites():
        logger.critical("Les sprites ne sont pas présents, veuillez les télécharger.")
        quit()

    logger.info("Vérification des noms des fichiers des sprites")
    misc.correct_sprites_filenames()

    client.tree.add_command(avatar)


db_objects = database.objects
