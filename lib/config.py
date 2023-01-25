"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging
import os

logger = logging.getLogger("libs.config")

config_variables = {
    "token": "DISCORD_BOT_TOKEN",
    "application_id": "DISCORD_APPLICATION_ID",
    "owner_id": "DISCORD_OWNER_ID",
    "main_guild_id": "DISCORD_MAIN_GUILD_ID",
    "status_channel_id": "DISCORD_STATUS_CHANNEL_ID",
    "database_name": "DATABASE_NAME",
    "database_user": "DATABASE_USER",
    "database_password": "DATABASE_PASSWORD",
    "database_host": "DATABASE_HOST",
    "database_port": "DATABASE_PORT",
    "database_ssl": "DATABASE_SSL",
    "environment": "ENVIRONMENT"
}


def get(config, *, log=True):
    """
    Renvoyer une valeur de configuration du bot.
    """
    if config in config_variables:
        if log:
            logger.debug(f"Récupération de la variable d'environnement {config}")
        return os.environ.get(f'{config_variables[config]}')
    else:
        if log:
            logger.warning(f"La variable de configuration {config} a été demandée mais n'existe pas.")
        return None
