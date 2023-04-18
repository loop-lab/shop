from models.base_model import BaseModel
from models.product import Product
from models.size import Size
from peewee import IntegerField, ForeignKeyField

class Product_Size(BaseModel):
    product_id = ForeignKeyField(Product)
    size_id = ForeignKeyField(Size)
    count = IntegerField()

    class Meta:
        db_table = 'product_sizes'
        primary_key = False