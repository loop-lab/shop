from models.base_model import BaseModel
from models.order import Order
from models.product import Product
from models.size import Size
from peewee import IntegerField, ForeignKeyField

class Order_Product(BaseModel):
    order_id = ForeignKeyField(Order)
    product_id = ForeignKeyField(Product)
    size_id = ForeignKeyField(Size)
    count = IntegerField()

    class Meta:
        db_table = 'order_products'
        primary_key = False