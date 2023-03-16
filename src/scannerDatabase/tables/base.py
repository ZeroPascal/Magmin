
import os
from pathlib import Path
from peewee import Model, SqliteDatabase

from definitions import EXE_DIR
print(EXE_DIR)
db = SqliteDatabase(os.path.join(EXE_DIR,'database.db'))

class BaseModle(Model):
    class Meta:
        database = db
