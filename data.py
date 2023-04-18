from main import db
from models import *
from peewee import InternalError


def create_db_table():
    try:
        db.create_tables([
            File,
            Order,
            Order_Product,
            Product,
            Product_File,
            Product_Size,
            Size,
            Status,
            User,
        ])
    except InternalError as px:
        print(str(px))


if __name__ == '__main__':
    db.connect()
    create_db_table()