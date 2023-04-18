import datetime
from models.base_model import BaseModel
from peewee import PrimaryKeyField, CharField, DateTimeField


class Status(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'statuses'
        order_by = ('created_at')