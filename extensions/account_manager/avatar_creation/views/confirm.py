"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
import extensions.account_manager.lib.visuals as visuals


class Confirmation(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.action = None
        self.interaction = None

    @discord.ui.button(emoji="♻️", label='Régénérer', style=discord.ButtonStyle.blurple, disabled=False)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = False
        self.interaction = interaction
        self.stop()

    @discord.ui.button(emoji="✅", label='Valider', style=discord.ButtonStyle.green, disabled=False)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = True
        self.interaction = interaction
        self.stop()

    @discord.ui.button(emoji="❎", label='Annuler', style=discord.ButtonStyle.red, disabled=False)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.action = "cancel"
        self.interaction = interaction
        self.stop()

