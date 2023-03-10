"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
from __future__ import annotations

import logging
import os.path
from typing import TYPE_CHECKING

import peewee
import playhouse.pool

if TYPE_CHECKING:
    from .extensions import Extension

logger = logging.getLogger("libs.database")
if os.environ.get("DATABASE_SSL") == "True":
    if os.path.exists("/app/data/ca.pem"):
        db = playhouse.pool.PooledMySQLDatabase(os.environ.get("DATABASE_NAME"),
                                                user=os.environ.get("DATABASE_USER"),
                                                password=os.environ.get("DATABASE_PASSWORD"),
                                                host=os.environ.get("DATABASE_HOST"),
                                                port=int(os.environ.get("DATABASE_PORT")),
                                                ssl_ca="/app/data/ca.pem",
                                                max_allowed_packet=1024 * 1024 * 64,  # 64MB
                                                field_types={'BLOB': 'LONGBLOB'},
                                                max_connections=32,
                                                stale_timeout=300
                                                )
        logger.info("Connection à la base de données (SSL activé).")
    else:
        logger.critical("Le fichier clé de l'autorité de certification SSL n'a pas été trouvé.")
        quit()
else:
    db = playhouse.pool.PooledMySQLDatabase(os.environ.get("DATABASE_NAME"),
                                            user=os.environ.get("DATABASE_USER"),
                                            password=os.environ.get("DATABASE_PASSWORD"),
                                            host=os.environ.get("DATABASE_HOST"),
                                            port=int(os.environ.get("DATABASE_PORT")),
                                            max_allowed_packet=1024 * 1024 * 64,  # 64MB
                                            field_types={'BLOB': 'LONGBLOB'},
                                            max_connections=32,
                                            stale_timeout=300
                                            )
    logger.info("Connection à la base de données (SSL désactivé).")


def initialise_db():
    try:
        db.connect()
    except peewee.OperationalError:
        logger.critical("Impossible de se connecter à la base de données.")
        quit()
    logger.info("Connection initiale à la base de données réussie.")
    logger.info("Création des tables manquantes dans la base de données.")
    db.create_tables([Config])
    logger.info("Création des tables terminée.")
    logger.info("Initialisation de la base de données terminée.")
    db.close()


def open_db():
    try:
        db.connect(True)
    except peewee.OperationalError:
        logger.critical("Impossible de se connecter à la base de données.")
        quit()
    logger.info("Connecté à la base de données.")


def close_db():
    db.close()
    logger.info("Déconnecté de la base de données.")


def create_tables(extension: Extension):
    """Créé les tables nécessaire pour l'extension indiquée."""
    open_db()
    for db_object in extension.db_objects:
        db.create_tables(db_object)
    close_db()


class BaseModel(peewee.Model):
    class Meta:
        database = db
        legacy_table_names = False


class Config(BaseModel):
    key = peewee.CharField()
    value = peewee.CharField()
