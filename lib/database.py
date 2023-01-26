"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import os.path
import logging
import peewee
from playhouse.mysql_ext import MySQLConnectorDatabase
import lib.config as config

logger = logging.getLogger("libs.database")
if config.get("database_ssl") == "True":
    if os.path.exists("/app/data/ca.pem"):
        db = MySQLConnectorDatabase(config.get("database_name"),
                                    user=config.get("database_user"),
                                    password=config.get("database_password"),
                                    host=config.get("database_host"),
                                    port=int(config.get("database_port")),
                                    ssl_ca="/app/data/ca.pem"
                                    )
    else:
        logger.critical("Le fichier clé de l'autorité de certification SSL n'a pas été trouvé.")
else:
    db = MySQLConnectorDatabase(config.get("database_name"),
                                user=config.get("database_user"),
                                password=config.get("database_password"),
                                host=config.get("database_host"),
                                port=int(config.get("database_port"))
                                )


def initialise_db():
    db.connect()
    db.create_tables([Avatar])


class BaseModel(peewee.Model):
    class Meta:
        database = db
        legacy_table_names = False


class Avatar(BaseModel):
    user_id = peewee.BigIntegerField()
    avatar = peewee.BlobField()
