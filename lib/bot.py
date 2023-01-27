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

from lib.monitoring import commands_ran, errors, messages_received


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

    async def on_app_command_error(self, interaction: discord.Interaction, command: app_commands.Command,
                                   error: Exception):
        # On incrémente le compteur d'erreurs
        errors.labels(error.__class__.__name__, command.name).inc()
        logging.exception("Une erreur est survenue lors de l'exécution d'une commande : %s", sys.exc_info())

    async def on_message(self, message: discord.Message):
        # On incrémente le compteur de messages reçus
        if message.guild is not None:
            messages_received.labels(message.guild.name).inc()
        else:
            messages_received.labels('Messages privés').inc()

    async def on_ready(self):
        # On lance la fonction de démarrage
        for guild in self.guilds:
            messages_received.labels(guild.name).inc()
        messages_received.labels('Messages privés').inc()
        for command in self.tree.get_commands():
            commands_ran.labels(command.name).inc()
