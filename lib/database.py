"""
Copyright © Aeris1One 2023 (Dandelion)

Ce programme est régi par la licence CeCILL soumise au droit français et
respectant les principes de diffusion des logiciels libres. Vous pouvez
utiliser, modifier et/ou redistribuer ce programme sous les conditions
de la licence CeCILL diffusée sur le site "http://www.cecill.info".
"""
import peewee
import lib.config as config

db = peewee.MySQLDatabase(config.get("database_name"),
                          user=config.get("database_user"),
                          password=config.get("database_password"),
                          host=config.get("database_host"),
                          port=int(config.get("database_port"))
                          )

# SQLite
# db = peewee.SqliteDatabase('/app/data/database.db')


def initialise_db():
    db.connect()
    db.create_tables([Avatar])


class BaseModel(peewee.Model):
    class Meta:
        database = db
        legacy_table_names = False


class Avatar(BaseModel):
    user_id = peewee.IntegerField()
    avatar = peewee.BlobField()
