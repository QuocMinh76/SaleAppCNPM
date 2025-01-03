from app.models import Category, Product, User, Receipt, ReceiptDetails, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime


def load_categories():
    return Category.query.order_by('id').all()


def load_products(cate_id=None, kw=None, page=1):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    page_size = app.config["PAGE_SIZE"]
    start = (page - 1) * page_size
    products = products.slice(start, start + page_size)

    return products.all()


def count_products():
    return Product.query.count()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password,
             avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg")

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get("secure_url")

    db.session.add(u)
    db.session.commit()


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)

        db.session.add(receipt)

        for c in cart.values():
            detail = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                                    product_id=c['id'], receipt=receipt)
            db.session.add(detail)

        db.session.commit()


def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password))

    if role:
        u = u.filter(User.user_role.__eq__(role))

    return u.first()


def get_user_by_id(id):
    return User.query.get(id)


def revenue_stats(kw=None):
    query = db.session.query(Product.id, Product.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id)).group_by(Product.id)

    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all()


def period_stats(p='month', year=datetime.now().year):
    return db.session.query(func.extract(p, Receipt.created_date),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
                        .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                        .group_by(func.extract(p, Receipt.created_date), func.extract('year', Receipt.created_date))\
                        .filter(func.extract('year', Receipt.created_date).__eq__(year)).all()


def stats_products():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True).group_by(Category.id).all()


def get_prod_by_id(id):
    return Product.query.get(id)


def load_comments(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id))


def add_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)

    db.session.add(c)
    db.session.commit()

    return c


# Chạy thử in kết quả hàm thống kê
if __name__ == '__main__':
    with app.app_context():
        print(stats_products())
