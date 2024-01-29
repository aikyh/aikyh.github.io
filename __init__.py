import mailbox
import bcrypt as Bcrypt
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from main import *
import os, shelve, Response, Product
from Forms import CreateCheckoutForm, CreateUpdateForm, CreateProductForm


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

    db.init_app(app)

    with app.app_context():
        db.create_all()

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        from models import User

        @login_manager.user_loader
        def load_user(user_id):
            return db.session.get(User, user_id)

        from auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        from admin import admin as admin_blueprint
        app.register_blueprint(admin_blueprint)


    app.run(debug=True, port=8000)


class Product:
    count_id = 0

    def __init__(self, name, price, image):
        Product.count_id += 1
        self.name = name
        self.price = price
        self.image = image


class Store:
    def __init__(self):
        self.products = shelve.open('products.db', writeback=True)

    def add_product(self, product):
        self.products[product.name] = product

    def get_product(self, name):
        print(self.products.get(name))
        return self.products.get(name)

    def get_all_products(self):
        return list(self.products.values())

    def close(self):
        self.products.close()


class Cart:
    def __init__(self):
        self.carts = shelve.open('carts.db', writeback=True)
        self.items = {}

    def save_cart(self, id):
        self.carts[id] = self.items

    def get_cart(self):
        return self.carts['1']

    def add_item(self, id, product):
        if '1' in self.carts:
            items = self.carts[id]
            if product.name in items:
                items[product.name]['quantity'] += 1
            else:
                items[product.name] = {'product': product, 'quantity': 1}
            print(items)
            self.carts[id] = items
        else:
            items[product.name] = {'product': product, 'quantity': 1}
            self.carts[id] = items

    def remove_item(self, id, product):
        items = self.carts[id]
        if product.name in items:
            if items[product.name]['quantity'] > 1:
                items[product.name]['quantity'] -= 1
            else:
                del items[product.name]
        self.carts[id] = items

    def get_items(self):
        return list(self.items.values())

    def clear(self):
        self.items = {}

    def close(self):
        self.carts.close()


@app.route('/store')
def store_page():
    store = Store()
    product = Product("tomato seed", 99999999, '../static/img/tomato seed.jpeg')
    store.add_product(product)
    product = Product("potato seed", 9999, '../static/img/potato seed.jpg')
    store.add_product(product)
    products = store.get_all_products()
    store.close()
    reviews_dict = {}
    db = shelve.open('review.db', 'r')
    reviews_dict = db['Reviews']
    db.close()
    reviews_list = []
    for key in reviews_dict:
        review = reviews_dict.get(key)
        reviews_list.append(review)

    return render_template('store.html', products=products, count=len(reviews_list), reviews_list=reviews_list)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    store = Store()
    cart = Cart()
    product_name = request.form['product_name']
    product = store.get_product(product_name)
    cart.add_item('1', product)
    store.close()
    cart.close()
    return redirect(url_for('cart_page'))


@app.route('/cart')
def cart_page():
    cart = Cart()
    items = list(cart.get_cart().values())

    # Calculate total price
    total_price = sum(item['product'].price * item['quantity'] for item in items)

    print(items)
    cart.close()
    return render_template('cart.html', items=items, total_price=total_price)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_name = request.form['product_name']

    store = Store()
    cart = Cart()
    print(store.get_all_products())
    product = store.get_product(product_name)
    cart.get_cart()
    cart.remove_item('1', product)
    store.close()
    cart.close()
    return redirect(url_for('cart_page'))

@app.route('/createReview', methods=['GET', 'POST'])
def create_review():
    create_review_form = CreateReviewForm(request.form)

    if request.method == 'POST' and create_review_form.validate():
        reviews_dict = {}
        db = shelve.open('review.db', 'c')

        try:
            reviews_dict = db['Reviews']
        except:
            print("Error in retrieving Reviews from review.db.")

        review = Review.Review(create_review_form.customer_name.data, create_review_form.product_name.data,
                               create_review_form.rating.data, create_review_form.email.data,
                               create_review_form.review_date.data, create_review_form.comments.data)
        reviews_dict[review.get_review_id()] = review
        db['Reviews'] = reviews_dict

        db.close()

        return redirect(url_for('retrieve_reviews'))

    return render_template('createReview.html', form=create_review_form)

@app.route('/retrieveReviews')
def retrieve_reviews():
    reviews_dict = {}
    db = shelve.open('review.db', 'r')
    reviews_dict = db['Reviews']
    db.close()
    reviews_list = []
    for key in reviews_dict:
       review = reviews_dict.get(key)
       reviews_list.append(review)

    return render_template('retrieveReviews.html', count=len(reviews_list), reviews_list=reviews_list)

@app.route('/updateReview/<int:id>/', methods=['GET', 'POST'])
def update_review(id):
    update_review_form = CreateReviewForm(request.form)

    if request.method == 'POST' and update_review_form.validate():
        reviews_dict = {}
        db = shelve.open('review.db', 'w')
        reviews_dict = db['Reviews']

        review = reviews_dict.get(id)
        review.set_customer_name(update_review_form.customer_name.data)
        review.set_product_name(update_review_form.product_name.data)
        review.set_rating(update_review_form.rating.data)
        review.set_email(update_review_form.email.data)
        review.set_review_date(update_review_form.review_date.data)
        review.set_comments(update_review_form.comments.data)

        db['Reviews'] = reviews_dict
        db.close()

        return redirect(url_for('retrieve_reviews'))
    else:
        reviews_dict = {}
        db = shelve.open('review.db', 'r')
        reviews_dict = db['Reviews']
        db.close()

        review = reviews_dict.get(id)
        update_review_form.customer_name.data = review.get_customer_name()
        update_review_form.product_name.data = review.get_product_name()
        update_review_form.rating.data = review.get_rating()
        update_review_form.email.data = review.get_email()
        update_review_form.review_date.data = review.get_review_date()
        update_review_form.comments.data = review.get_comments()

        return render_template('updateReview.html', form=update_review_form)

@app.route('/deleteReview/<int:id>', methods=['POST'])
def delete_review(id):
    reviews_dict = {}
    db = shelve.open('review.db', 'w')
    reviews_dict = db.get('Reviews', {})

    reviews_dict.pop(id)

    db['Reviews'] = reviews_dict

    db.close()

    return redirect(url_for('retrieve_reviews'))


@app.route('/review')
def reply_review():
     reviews_dict = {}
     db = shelve.open('review.db', 'r')
     reviews_dict = db['Reviews']
     db.close()
     reviews_list = []
     for key in reviews_dict:
       review = reviews_dict.get(key)
       reviews_list.append(review)

     return render_template('productmanagement.html', count=len(reviews_list), reviews_list=reviews_list)



if __name__ == '__main__':
    create_app()
