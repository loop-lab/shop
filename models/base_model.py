from peewee import Model

class BaseModel(Model):
    class Meta:
        from main import db
        database = db