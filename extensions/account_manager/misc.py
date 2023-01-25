"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import lib.visuals as visuals
import lib.avatars as avatars
import extensions.account_manager.main_menu.main as main_menu


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
    action, interaction = await main_menu.confirm(interaction)
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
