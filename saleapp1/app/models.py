from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum
from app import db, app
import hashlib
from enum import Enum as RoleEnum

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), nullable=True)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # add user
        u = User(name="admin", username="admin", password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()),
                 avatar="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
                 user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        # add categories
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Tablet")
        # c3 = Category(name="Desktop")
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # add products
        # data = [{
        #     "id": 1,
        #     "name": "iPhone 7 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 2,
        #     "name": "iPad Pro 2020",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #     "category_id": 2
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 10",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 10 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 11",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 11 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 1,
        #     "name": "iPhone 8 Plus",
        #     "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #     "price": 17000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 2,
        #     "name": "iPad Pro 2024",
        #     "description": "Apple, 128GB, RAM: 6GB",
        #     "price": 37000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #     "category_id": 2
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 20",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 20 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 21",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }, {
        #     "id": 3,
        #     "name": "Galaxy Note 21 Plus",
        #     "description": "Samsung, 64GB, RAML: 6GB",
        #     "price": 24000000,
        #     "image":
        #         "https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #     "category_id": 1
        # }]
        #
        # for p in data:
        #     prod = Product(name=p['name'], description=p['description'], price=p['price'],
        #                    image=p['image'], category_id=p['category_id'])
        #     db.session.add(prod)
        #
        # db.session.commit()