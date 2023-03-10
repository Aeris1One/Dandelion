"""
Copyright © Aeris1One 2023 (Dandelion)
Copyright © ascpial 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import logging
import os

import lib.database as database

logger = logging.getLogger("libs.config")

config_variables = {
    "token": "DISCORD_BOT_TOKEN",
    "application_id": "DISCORD_APPLICATION_ID",
    "owner_id": "DISCORD_OWNER_ID",
    "main_guild_id": "DISCORD_MAIN_GUILD_ID",
    "status_channel_id": "DISCORD_STATUS_CHANNEL_ID",
    "environment": "ENVIRONMENT",
    "proxy": "PROXY",
}


def get(config, *, log=True):
    """
    Renvoyer une valeur de configuration du bot.

    Si la variable d'environnement existe, elle est renvoyée.
    Sinon, la clé en base de données est renvoyée.

    :param config: La clé de la variable de configuration à récupérer.
    :param log: Si False, les logs ne seront pas affichés (utile si appelé avant la configuration du logger).
    """
    # Variable d'environnement
    if config in config_variables:
        if log:
            logger.debug(f"Récupération de la variable d'environnement {config}")
        return os.environ.get(f'{config_variables[config]}')

    # Variable en base de données
    if log:
        logger.debug(f"La variable de configuration {config} a été demandée mais n'existe pas dans les variables "
                     f"d'environnement.")
    try:
        return database.Config().get(database.Config.key == config).value
    except database.peewee.DoesNotExist:
        logger.warning(f"La variable de configuration {config} n'existe pas dans la base de données.")
        return None


def set(config, value):
    """
    Définir une valeur de configuration du bot.
    La clé est définie en base de données, en remplacant la valeur si elle existe déjà.

    :param config: La clé de la variable de configuration à définir.
    :param value: La valeur de la variable de configuration à définir.
    """
    logger.debug(f"La variable de configuration {config} va être définie à {value}.")
    try:
        database.Config().update(value=value).where(database.Config.key == config).execute()
        logger.debug(f"La variable de configuration {config} a été mise à jour vers {value}.")
    except database.peewee.DoesNotExist:
        logger.debug(f"La variable de configuration {config} n'existe pas dans la base de données, elle va être créée.")
        database.Config().create(key=config, value=value)
        logger.debug(f"La variable de configuration {config} a été créée avec la valeur {value}.")


def delete(config):
    """
    Supprimer une valeur de configuration du bot.
    La clé est supprimée de la base de données.

    :param config: La clé de la variable de configuration à supprimer.
    """
    logger.debug(f"La variable de configuration {config} va être supprimée.")
    try:
        database.Config().delete().where(database.Config.key == config).execute()
        logger.debug(f"La variable de configuration {config} a été supprimée.")
    except database.peewee.DoesNotExist:
        logger.warning(f"La variable de configuration {config} devait être supprimée mais elle n'existe pas dans la "
                       f"base de données.")


def get_proxy() -> dict[str, str] | None:
    proxy = get('proxy')

    if proxy != "":
        return {
            "http": proxy,
            "https": proxy,
        }
    else:
        return None
