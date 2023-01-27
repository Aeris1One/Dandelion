"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
from discord import Interaction

import lib.visuals as visuals
import lib.avatars as avatars


class MenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.action = None
        self.interaction = None

    @discord.ui.button(emoji="♻️", label='Changer d\'avatar', style=discord.ButtonStyle.green, disabled=False)
    async def change_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = "create_avatar"
        self.interaction = interaction
        self.stop()

    @discord.ui.button(emoji="🗑️", label='Le supprimer', style=discord.ButtonStyle.danger, disabled=False)
    async def delete_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = "delete_avatar"
        self.interaction = interaction
        self.stop()

    @discord.ui.button(emoji="🤷‍♂️", label='Rien', style=discord.ButtonStyle.blurple, disabled=False)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = "nothing"
        self.interaction = interaction
        self.stop()


class MenuNoAvatarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.interaction = None
        self.action = None

    @discord.ui.button(emoji="♻️", label='Créer mon avatar !', style=discord.ButtonStyle.green, disabled=False)
    async def change_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = "create_avatar"
        self.interaction = interaction
        self.stop()

    @discord.ui.button(emoji="🤷‍♂️", label='Rien', style=discord.ButtonStyle.blurple, disabled=False)
    async def do_nothing(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = "nothing"
        self.interaction = interaction
        self.stop()


async def menu(interaction: discord.Interaction) -> tuple[str, Interaction]:
    if avatars.user_has_avatar(interaction.user.id):
        view = MenuView()
        await interaction.response.send_message(file=visuals.generate_bubble_with_avatar("happy",
                                                                                         "Tu as déjà un avatar, que "
                                                                                         "veux-tu faire ?\nUtilises "
                                                                                         "les boutons pour faire ton "
                                                                                         "choix !",
                                                                                         userid=interaction.user.id),
                                                view=view, ephemeral=True)
    else:
        view = MenuNoAvatarView()
        await interaction.response.send_message(file=visuals.generate_bubble("happy",
                                                                             "Tu n'as pas encore d'avatar, veux-tu en\n"
                                                                             "créer un ?\n"
                                                                             "Utilises les boutons pour faire ton choix"),
                                                view=view, ephemeral=True)
    await view.wait()
    if view.action is None:
        return 'timeout', interaction
    return view.action, view.interaction

