"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
from discord import app_commands


class DandelionClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # On définit l'arbre de commandes
        self.tree = app_commands.CommandTree(self)
        self.config = {}

    async def setup_hook(self):
        # On synchronise les commandes avec l'API
        await self.tree.sync()
