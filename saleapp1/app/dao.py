from app.models import Category, Product


def load_categories():
    return Category.query.order_by('id').all()


def load_products(kw=None):
    products = Product.query

    if kw:
        products = products.filter(Product.name.contains(kw))

    return products.all()
