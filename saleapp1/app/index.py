import math

from flask import render_template, request, redirect
import dao
from app import app


@app.route("/")
def index():
    cates = dao.load_categories()

    page = request.args.get('page', 1)
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    prods = dao.load_products(cate_id= cate_id, kw=kw, page=int(page))

    page_size = app.config["PAGE_SIZE"]
    total = dao.count_products()

    return render_template('index.html', categories=cates, products=prods, pages=math.ceil(total/page_size))

@app.route("/register", methods=['get', 'post'])
def register_view():
    err_msg = ''

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not password.__eq__(confirm):
            err_msg = 'Mật khẩu không khớp!'
        else:
            data = request.form.copy()

            del data['confirm']
            dao.add_user(**data)
            return redirect('/login')

    return render_template('register.html', err_msg=err_msg)

@app.route("/login")
def login_view():
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)