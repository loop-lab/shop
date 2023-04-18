import datetime
from models.base_model import BaseModel
from peewee import PrimaryKeyField, BigIntegerField, CharField, DateTimeField


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    phone = BigIntegerField()
    tg_id = CharField(max_length=100, null=True)
    coins = BigIntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'users'
        order_by = ('created_at')