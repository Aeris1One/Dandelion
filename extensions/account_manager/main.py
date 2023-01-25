"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import extensions.account_manager.main_menu.main as main_menu
import extensions.account_manager.avatar_creation.main as avatar_creation
import extensions.account_manager.misc as misc


def main(client):
    @client.tree.command(
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
