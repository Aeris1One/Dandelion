"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
from discord import app_commands
import sys
import logging

from lib.monitoring import commands_ran,errors


class DandelionClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # On définit l'arbre de commandes
        self.tree = app_commands.CommandTree(self)
        self.config = {}

    async def setup_hook(self):
        # On synchronise les commandes avec l'API
        await self.tree.sync()

    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        # On incrémente le compteur de commandes exécutées
        commands_ran.labels(command.name).inc()

    async def on_error(self, event_method: str, *args, **kwargs) -> None:
        # Retrieve exception type
        exception_type = sys.exc_info()[0]

        # On incrémente le compteur d'erreurs
        errors.labels(exception_type, event_method).inc()
        logging.exception("Une erreur est survenue lors de l'exécution d'un événement : %s", sys.exc_info())