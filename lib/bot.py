"""
Copyright © Aeris1One 2023 (Dandelion)
Copyright © ascpial 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import discord
from discord import app_commands
import sys
import logging

from .monitoring import commands_ran, errors, messages_received
from .extensions import Extension
from .database import create_tables

logger = logging.getLogger("bot")

class DandelionClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, proxy: str = ""):
        super().__init__(intents=intents, proxy=proxy)
        # On définit l'arbre de commandes
        self.tree = app_commands.CommandTree(self)
        self.config = {}
        self.extensions: list[Extension] = []

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
            logger.debug("Message reçu sur le serveur %s, incrémentation du compteur de messages reçus", message.guild.name)
            messages_received.labels(message.guild.name).inc()
        else:
            logger.debug("Message privé reçu, incrémentation du compteur de messages privés")
            messages_received.labels('Messages privés').inc()

    async def on_ready(self):
        # On lance la fonction de démarrage
        for guild in self.guilds:
            logger.debug("Initialisation du monitoring, incrémentation du compteur de messages reçus pour le serveur %s",
                         guild.name)
            messages_received.labels(guild.name).inc()
        logger.debug("Initialisation du monitoring, incrémentation du compteur de messages privés")
        messages_received.labels('Messages privés').inc()
        for command in self.tree.get_commands():
            logger.debug("Initialisation du monitoring, incrémentation du compteur de commandes exécutées pour la "
                         "commande %s", command.name)
            commands_ran.labels(command.name).inc()

    def load_extension(self, namespace: str) -> Extension:
        """Charge une extension depuis le dossier par défaut.
        
        Attention ! Cette fonction n'est pas l'implémentation par défaut de
        discord.py !
        """
        extension = Extension(namespace)
        extension.load()

        create_tables(extension)

        extension.register(self)

        self.extensions.append(extension)
