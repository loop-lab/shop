import datetime
from models.base_model import BaseModel
from peewee import PrimaryKeyField, IntegerField, CharField, DateTimeField


class Product(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    price = IntegerField()
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'products'
        order_by = ('created_at')