from models import Order, Product, Size, User, Order_Product

def setOrder(tg_id, data):
    user_id = User.get(User.tg_id == tg_id).id
    order = Order(
        total_price=data['total'],
        user_id=user_id,
        status_id=1
    )
    order.save()
    products = []
    for product in data['products']:
        products.append({
            'order_id': order.id,
            'product_id': product['id'],
            'size_id': product['size'],
            'count': product['count'],
        })
    return Order_Product().insert_many(products).execute()


def getProductsById(ids):
    return Product.select().where(Product.id.in_(ids)).dicts()


def getSizesById(ids):
    return Size.select().where(Size.id.in_(ids)).dicts()

def updateStatusOrder(user_id, status_id):
    Order.update(status_id = status_id).where(Order.user_id == user_id).execute()\


def hasActiveOrder(user_id):
    return Order.select().where(Order.status_id.in_([1,2]), Order.user_id == user_id).exists()