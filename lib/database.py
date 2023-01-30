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

logger = logging.getLogger("libs.database")
if os.environ.get("DATABASE_SSL") == "True":
    if os.path.exists("/app/data/ca.pem"):
        try:
            db = peewee.MySQLDatabase(os.environ.get("DATABASE_NAME"),
                                      user=os.environ.get("DATABASE_USER"),
                                      password=os.environ.get("DATABASE_PASSWORD"),
                                      host=os.environ.get("DATABASE_HOST"),
                                      port=int(os.environ.get("DATABASE_PORT")),
                                      ssl_ca="/app/data/ca.pem",
                                      max_allowed_packet=1024 * 1024 * 64,  # 64MB
                                      field_types={'BLOB': 'LONGBLOB'}
                                      )
            logger.info("Connecté à la base de données (SSL activé).")
        except peewee.OperationalError:
            logger.critical("Impossible de se connecter à la base de données.")
            quit()
    else:
        logger.critical("Le fichier clé de l'autorité de certification SSL n'a pas été trouvé.")
        quit()
else:
    try:
        db = peewee.MySQLDatabase(os.environ.get("DATABASE_NAME"),
                                  user=os.environ.get("DATABASE_USER"),
                                  password=os.environ.get("DATABASE_PASSWORD"),
                                  host=os.environ.get("DATABASE_HOST"),
                                  port=int(os.environ.get("DATABASE_PORT")),
                                  max_allowed_packet=1024 * 1024 * 64,  # 64MB
                                  field_types={'BLOB': 'LONGBLOB'}
                                  )
        logger.info("Connecté à la base de données (SSL désactivé).")
    except peewee.OperationalError:
        logger.critical("Impossible de se connecter à la base de données.")
        quit()


def initialise_db():
    db.connect()
    logger.info("Création des tables manquantes dans la base de données.")
    db.create_tables([Avatar])


class BaseModel(peewee.Model):
    class Meta:
        database = db
        legacy_table_names = False


class Avatar(BaseModel):
    user_id = peewee.BigIntegerField()
    avatar = peewee.BlobField()


class Config(BaseModel):
    key = peewee.CharField()
    value = peewee.CharField()
