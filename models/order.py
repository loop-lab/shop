import datetime
from models.base_model import BaseModel
from models.user import User
from models.status import Status
from peewee import PrimaryKeyField, BigIntegerField, DateTimeField, ForeignKeyField


class Order(BaseModel):
    id = PrimaryKeyField(null=False)
    total_price = BigIntegerField()
    user_id = ForeignKeyField(User)
    status_id = ForeignKeyField(Status)
    created_at = DateTimeField(default=datetime.datetime.now())
    updated_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'orders'
        order_by = ('created_at')