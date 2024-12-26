from peewee import * 

db_name='diary_bd'
user='postgres'
password='123'
host='localhost'
port=5432
# Инициализация БД
db = PostgresqlDatabase(db_name, user=user, password=password, host=host, port=port)

class BaseModel(Model):
    class Meta:
        database = db
