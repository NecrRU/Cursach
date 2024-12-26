from peewee import *
import playhouse.postgres_ext as pg
from config import BaseModel, db

class VarcharArrayField(Field):
	db_field = 'varchar(20)[]'
	def db_value(self, value):
		return value
	def python_value(self, value):
		return value


class Account(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(unique=True)
    password = CharField()

    class Meta:
        db_table = "accounts"

class Compilation(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    description = TextField(null = True)
    account_id = ForeignKeyField(Account, on_delete='cascade')

    class Meta:
        db_table = "compilations"

class Product(BaseModel):
    compilation_id = ForeignKeyField(Compilation, on_delete='cascade')
    id = AutoField(primary_key=True)
    type = CharField(null = True)
    name = CharField()
    author = CharField(null = True)
    genre = pg.ArrayField(field_class=CharField, null = True)
    release_date = DateField(null = True)
    description = TextField(null = True)
    personal_rating = IntegerField(null = True)
    aggregator_rating = IntegerField(null = True)
    personal_review = TextField(null = True)


    class Meta:
        db_table = "products"

with db:
    db.create_tables([Account, Compilation, Product])
