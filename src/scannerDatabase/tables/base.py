
import os
from pathlib import Path
from peewee import Model, SqliteDatabase

from definitions import ROOT_DIR

db = SqliteDatabase(os.path.join(ROOT_DIR,'database.db'))

class BaseModle(Model):
    class Meta:
        database = db
