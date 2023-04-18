from models.base_model import BaseModel
from peewee import PrimaryKeyField, CharField


class File(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    path = CharField(max_length=255)

    class Meta:
        db_table = 'files'
        order_by = ('created_at')