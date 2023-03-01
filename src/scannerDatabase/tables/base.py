
from peewee import Model, SqliteDatabase

    
db = SqliteDatabase('./database.db')

class BaseModle(Model):
    class Meta:
        database = db
