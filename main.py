"""
Copyright © Aeris1One 2023 (Dandelion)
Copyright © ascpial 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging
import logging.handlers
import os

import discord

import lib.config as config
import lib.data as data
from lib.bot import DandelionClient
from lib.database import initialise_db
from lib.extensions import available_namespaces
from lib.monitoring import init_prometheus


def main():
    # On initialise les logs
    if not os.path.exists("/app/data/logs"):
        os.mkdir("/app/data/logs")
    logger = logging.getLogger()

    if config.get("environment", log=False) == "production":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
        # Les logs de discord sont trop verbeux, même en débug
        logging.getLogger('discord.gateway').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.INFO)

    file_handler = logging.handlers.RotatingFileHandler(
        filename='/app/data/logs/dandelion.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    file_handler.setFormatter(logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', style='{'))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', style='{'))
    logger.addHandler(console_handler)

    # Gérer les données
    logger.info("Création de la structure de données")
    data.create_data_structure()

    logger.info("Suppression des fichiers temporaires")
    data.clear_tmp()

    logger.info("Téléchargement des données nécessaires")
    data.download_data()

    # On définit les intents nécessaires et le serveur mandataire
    intents = discord.Intents.default()
    client = DandelionClient(
        intents=intents,
        proxy=config.get("proxy"),
    )

    # On initialise la base de données
    logger.info("Initialisation de la base de données")
    initialise_db()

    # On charge les extensions
    logger.info("Chargement des extensions")
    for namespace in available_namespaces():
        client.load_extension(namespace)

    client.register_extensions()

    # On initialise Prometheus
    logger.info("Initialisation de Prometheus")
    init_prometheus()

    # On lance le bot
    logger.info("Lancement du bot")
    client.run(config.get("token"), reconnect=True, log_handler=None)


if __name__ == "__main__":
    main()
