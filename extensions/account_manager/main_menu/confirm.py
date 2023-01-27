"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import lib.visuals as visuals


class Confirmation(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.action = None
        self.interaction = None

    @discord.ui.button(emoji="🟥", label='Oui, supprimer mon avatar', style=discord.ButtonStyle.red, disabled=False)
    async def change_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = True
        self.interaction = interaction
        self.stop()

    @discord.ui.button(emoji="⬛", label='Annuler', style=discord.ButtonStyle.grey, disabled=False)
    async def do_nothing(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = False
        self.interaction = interaction
        self.stop()


async def confirm(interaction: discord.Interaction):
    view = Confirmation()
    await interaction.response.edit_message(attachments=[visuals.generate_bubble_with_avatar("happy",
                                                                                     "Tu as déjà un avatar, que "
                                                                                     "veux-tu faire ?\nUtilises "
                                                                                     "les boutons pour faire ton "
                                                                                     "choix !",
                                                                                     userid=interaction.user.id)],
                                            view=view)
    await view.wait()
    if view.action is None:
        return 'timeout', interaction
    return view.action, view.interaction

