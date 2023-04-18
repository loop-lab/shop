from models.base_model import BaseModel
from models.product import Product
from models.file import File
from peewee import ForeignKeyField

class Product_File(BaseModel):
    product_id = ForeignKeyField(Product)
    file_id = ForeignKeyField(File)

    class Meta:
        db_table = 'product_files'
        primary_key = False