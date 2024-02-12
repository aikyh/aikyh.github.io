import mailbox
import bcrypt as Bcrypt
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from main import *
from werkzeug.utils import secure_filename
import os, shelve, Response, eventManagement, Purchase, userEvents, RegisteredEventUser
from Forms import CreateCheckoutForm, CreateUpdateForm, CreateProductForm, CreateReviewForm, CreateEventForm, \
    CheckInForm, CreateUpdateForm2, CreateCheckoutForm2, RegsisterForm, Signupeventform
import Review, Cart, Store, Product

app = Flask(__name__)


def create_app():
    # app = Flask(__name__)
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
            self.items[product.name] = {'product': product, 'quantity': 1}
            self.carts[id] = self.items

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


# Event management - Admin
@app.route('/createEvents', methods=['GET', 'POST'])
def create_events():
    create_event_form = CreateEventForm(request.form)

    if request.method == 'POST' and create_event_form.validate():

        eventManagement_dict = {}
        db = shelve.open('eventManagement.db', 'c')

        try:
            eventManagement_dict = db['Events']
        except:
            print("Error in retrieving Events from eventManagement.db.")

        event = eventManagement.eventManagement(create_event_form.name.data, create_event_form.date.data,
                                                create_event_form.timing.data, create_event_form.location.data,
                                                create_event_form.description.data,
                                                create_event_form.budget.data, create_event_form.collaborators.data,
                                                create_event_form.person_in_charge.data)
        eventManagement_dict[event.get_event_id()] = event
        db['Events'] = eventManagement_dict

        db.close()

        return redirect(url_for('retrieve_events'))
    return render_template('createEvents.html', form=create_event_form, )


@app.route('/retrieveEvents')
def retrieve_events():
    eventManagement_dict = {}
    try:
        db = shelve.open('eventManagement.db', 'r')
        if 'Events' in db:
            eventManagement_dict = db['Events']
        else:
            db['Events'] = eventManagement_dict
        db.close()
    except:
        print("eventManagement.db not found")

    events_list = []
    for key in eventManagement_dict:
        events = eventManagement_dict.get(key)
        events_list.append(events)

    return render_template('retrieveEvents.html', count=len(events_list), events_list=events_list)


@app.route('/updateEvents/<int:id>/', methods=['GET', 'POST'])
def update_events(id):
    update_event_form = CreateEventForm(request.form)
    if request.method == 'POST' and update_event_form.validate():
        eventManagement_dict = {}
        db = shelve.open('eventManagement.db', 'w')
        eventManagement_dict = db['Events']

        event = eventManagement_dict.get(id)
        event.set_name(update_event_form.name.data)
        event.set_date(update_event_form.date.data)
        event.set_timing(update_event_form.timing.data)
        event.set_location(update_event_form.location.data)
        event.set_description(update_event_form.description.data)
        event.set_budget(update_event_form.budget.data)
        event.set_person_in_charge(update_event_form.person_in_charge.data)
        event.set_collaborators(update_event_form.collaborators.data)

        db['Events'] = eventManagement_dict
        db.close()

        return redirect(url_for('retrieve_events'))
    else:
        eventManagement_dict = {}
        db = shelve.open('eventManagement.db', 'r')
        eventManagement_dict = db['Events']
        db.close()

        event = eventManagement_dict.get(id)
        update_event_form.name.data = event.get_name()
        update_event_form.date.data = event.get_date()
        update_event_form.timing.data = event.get_timing()
        update_event_form.location.data = event.get_location()
        update_event_form.description.data = event.get_description()
        update_event_form.budget.data = event.get_budget()
        update_event_form.person_in_charge.data = event.get_person_in_charge()
        update_event_form.collaborators.data = event.get_collaborators()

        return render_template('updateEvents.html', form=update_event_form)


@app.route('/deleteEvent/<int:id>', methods=['POST'])
def delete_event(id):
    eventManagement = {}
    db = shelve.open('eventManagement.db', 'w')
    eventManagement_dict = db['Events']

    eventManagement_dict.pop(id)

    db['Events'] = eventManagement_dict
    db.close()

    return redirect(url_for('retrieve_events'))


# Events- User side

@app.route('/discoverEvents_confirmation')
def discoverEvents_confirmation():
    return render_template('discoverEvents_confirmation.html')


# @app.route('/retrieveDiscoverEvents', methods=['GET', 'POST'])
# def createDiscoverEvents():
#     discovereventsform = RegsisterForm(request.form)
#     if request.method == 'POST' and discovereventsform.validate():
#         discoverEvents_dict = {}
#         discovereventsdb = shelve.open('discoverevents.db', 'c')
#
#         try:
#             discoverEvents_dict = discovereventsdb['discoverevents']
#         except:
#             print("Error in retrieving discoverevents from discoverevents.db")
#
#         discoverEvents = userEvents.CheckIn(discovereventsform.name.data, discovereventsform.email.data)
#         discoverEvents_dict[discoverEvents.get_checkin_id()] = discoverEvents
#         discovereventsdb['discoverevents'] = discoverEvents_dict
#
#         discovereventsdb.close()
#     else:
#         return render_template('retrieveDiscoverEvents.html', form=discovereventsform)
#
#
# @app.route('/retrieveDiscoverEvents')
# def retrieve_userevents():
#     eventManagement_dict = {}
#     try:
#         db = shelve.open('eventManagement.db', 'r')
#         if 'Events' in db:
#             eventManagement_dict = db['Events']
#         else:
#             print("No events found in eventManagement.db")
#     except FileNotFoundError:
#         print("eventManagement.db not found")
#     except Exception as e:
#         print(f"Error retrieving events: {e}")
#     finally:
#         db.close()
#
#     # Print the retrieved events
#     for key, event in eventManagement_dict.items():
#         print(f"Event ID: {key}")
#         print(f"Name: {event.get_name()}")
#         print(f"Date: {event.get_date()}")
#         print(f"Timing: {event.get_timing()}")
#         print(f"Location: {event.get_location()}")
#         print(f"Description: {event.get_description()}")
#         print(f"Budget: {event.get_budget()}")
#         print(f"Person in Charge: {event.get_person_in_charge()}")
#         print(f"Collaborators: {event.get_collaborators()}")
#         print("-----------------------------")
#
#     events_list = list(eventManagement_dict.values())
#
#     return render_template('retrieveDiscoverEvents.html', count=len(events_list), events_list=events_list)


@app.route('/retrieveDiscoverEvents')
def retrieve_userEvents():
    event_dict = {}
    try:
        db = shelve.open('eventManagement.db', 'r')
        if 'Events' in db:
            event_dict = db['Events']
        else:
            db['Events'] = event_dict
        db.close()
    except:
        print("eventManagement.db not found")

    events_list = []
    for key in event_dict:
        events = event_dict.get(key)
        events_list.append(events)

    return render_template("retrieveDiscoverEvents.html", count=len(events_list), events_list=events_list)


@app.route('/userSignupEvents', methods=['GET', 'POST'])
def user_signup():
    userSignup_event_form = Signupeventform(request.form)

    if request.method == 'POST' and userSignup_event_form.validate():

        eventuser_dict = {}
        db = shelve.open('RegisteredEventUser.db', 'c')

        try:
            eventuser_dict = db['Events']
        except:
            print("Error in retrieving Events from RegisteredEventUser.db.")

        event = RegisteredEventUser.RegisteredEventUser(userSignup_event_form.name.data,
                                                        userSignup_event_form.email.data,
                                                        userSignup_event_form.no_of_people.data,
                                                        userSignup_event_form.contact_number.data)
        eventuser_dict[event] = event
        db['Events'] = eventManagement_dict

        db.close()

        return redirect(url_for('retrieve_events'))
    return render_template('createEvents.html', form=create_event_form, )


# @app.route('/registerevent')
# def registerevent():
#     return


# @app.route('/retrieveUserEvents')
# def createUserCheckIn():
#     create_checkIn_form = CheckInForm(request.form)
#     if request.method == 'POST' and create_checkIn_form.validate():
#         userCheckIn_dict = {}
#         db = shelve.open('usercheckIn.db', 'c')
#
#         try:
#             userCheckIn_dict = db['userCheckIn']
#
#         except:
#             print("Error in retrieving userCheckIn from usercheckIn.db")
#
#         userCheckIn = userEvents.CheckIn(create_checkIn_form.name.data, create_checkIn_form.email.data)
#         userCheckIn_dict[userCheckIn.get_checkin_id()] = userCheckIn
#         db['userCheckIn'] = userCheckIn_dict
#
#         db.close()
#
#     else:
#         return render_template('retrieveUserEvents.html', form=create_checkIn_form)

def retrieveUserCheckIn():
    userCheckIn_dict = {}
    try:
        db = shelve.open('userCheckIn.db', 'r')
        if 'userCheckIn' in db:
            userCheckIn_dict = db['userCheckIns']
        else:
            db['userCheckIn'] = userCheckIn_dict
        db.close()
    except:
        print('userCheckIn.db not found')

    userCheckIn_list = []
    for key in userCheckIn_list:
        userCheckIn = userCheckIn_dict.get(key)
        userCheckIn_dict.append(userCheckIn)

    return render_template('retrieveUserEvents.html', count=len(userCheckIn_list),
                           userCheckIn_list=userCheckIn_list)


@app.route('/userevent_confirmation', methods=['GET', 'POST'])
def userevent_confirmation():
    return render_template('confirmation.html')


@app.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file and allowed_file(file.filename):  # Add file extension validation
        filename = secure_filename(file.filename)

        # Save file data using shelve
        with shelve.open("files", "c") as db:
            db[filename] = file.read()

        flash("File uploaded successfully!")
    else:
        flash("Invalid file format or error during processing.")
    return redirect('/userevent_confirmation')


# Define allowed file extensions (optional)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg"]  # Add your allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS


@app.route('/donation')
# get method to get donation page
def donation():
    return render_template("donation.html")


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/success2')
def success2():
    return render_template("success2.html")


@app.route('/checkout', methods=['GET', 'POST'])
# accepts both get and post methods, checkout page is retrieved
# when form is received, data will be posted onto the server
def response():
    # Retrieve the 'amount' parameter
    amount = request.args.get('amount')
    create_checkout_form = CreateCheckoutForm(request.form)  # class object, calls server and passes in request
    default_amount = amount
    # Set the default value for amount
    create_checkout_form.amount.data = default_amount

    if request.method == 'POST' and create_checkout_form.validate():
        responses_dict = {}
        db = shelve.open('response.db', 'c')

        try:
            responses_dict = db['Responses']
        except:
            print("Error in retrieving Responses from response.db.")

        response = Response.Response(create_checkout_form.fname.data, create_checkout_form.lname.data,
                                     create_checkout_form.phone.data, create_checkout_form.email.data,
                                     create_checkout_form.add1.data, create_checkout_form.add2.data,
                                     create_checkout_form.pcode.data, create_checkout_form.dmethod.data,
                                     create_checkout_form.amount.data)
        responses_dict[response.get_response_id()] = response

        db['Responses'] = responses_dict

        db.close()

        return redirect(url_for('success'))

    return render_template('checkout.html', form=create_checkout_form, customAmount=amount)


@app.route('/responseManagement')
def response_management():
    responses_dict = {}
    db = shelve.open('response.db', 'r')
    responses_dict = db['Responses']
    db.close()

    responses_list = []
    for key in responses_dict:
        response = responses_dict.get(key)
        responses_list.append(response)

    return render_template('responseManagement.html', count=len(responses_list), responses_list=responses_list)


@app.route('/updateResponse/<int:id>/', methods=['GET', 'POST'])
def update_response(id):
    update_checkout_form = CreateUpdateForm(request.form)
    if request.method == 'POST' and update_checkout_form.validate():
        responses_dict = {}
        db = shelve.open('response.db', 'w')
        responses_dict = db['Responses']

        response = responses_dict.get(id)
        response.set_fname(update_checkout_form.fname.data)
        response.set_lname(update_checkout_form.lname.data)
        response.set_phone(update_checkout_form.phone.data)
        response.set_email(update_checkout_form.email.data)
        response.set_add1(update_checkout_form.add1.data)
        response.set_add2(update_checkout_form.add2.data)
        response.set_pcode(update_checkout_form.pcode.data)
        response.set_dmethod(update_checkout_form.dmethod.data)

        db['Responses'] = responses_dict
        db.close()

        return redirect(url_for('response_management'))
    else:
        responses_dict = {}
        db = shelve.open('response.db', 'r')
        responses_dict = db['Responses']
        db.close()

        response = responses_dict.get(id)
        update_checkout_form.fname.data = response.get_fname()
        update_checkout_form.lname.data = response.get_lname()
        update_checkout_form.phone.data = response.get_phone()
        update_checkout_form.email.data = response.get_email()
        update_checkout_form.add1.data = response.get_add1()
        update_checkout_form.add2.data = response.get_add2()
        update_checkout_form.pcode.data = response.get_pcode()
        update_checkout_form.dmethod.data = response.get_dmethod()

    return render_template('updateResponse.html', form=update_checkout_form)


@app.route('/deleteResponse/<int:id>', methods=['POST'])
def delete_response(id):
    responses_dict = {}
    db = shelve.open('response.db', 'w')
    responses_dict = db['Responses']

    responses_dict.pop(id)

    db['Responses'] = responses_dict
    db.close()

    return redirect(url_for('response_management'))


@app.route('/createProduct', methods=['GET', 'POST'])
# accepts both get and post methods, createProduct page is retrieved
# when form is received, data will be posted onto the server
def create_product():
    create_product_form = CreateProductForm(request.form)  # class object, calls server and passes in request
    if request.method == 'POST' and create_product_form.validate():

        products_dict = {}
        db = shelve.open('product.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from product.db.")

        product = Product.Product(create_product_form.name.data, create_product_form.price.data,
                                  create_product_form.description.data, create_product_form.tags.data)
        products_dict[product.get_product_id()] = product
        db['Products'] = products_dict

        db.close()

        return redirect(url_for('product_management'))
    return render_template('createProduct.html', form=create_product_form)


@app.route('/productManagement')
def product_management():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('productManagement.html', count=len(products_list), products_list=products_list)


@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_name(update_product_form.name.data)
        product.set_price(update_product_form.price.data)
        product.set_description(update_product_form.description.data)
        product.set_tags(update_product_form.tags.data)

        db['Products'] = products_dict
        db.close()

        return redirect(url_for('product_management'))
    else:
        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)
        update_product_form.name.data = product.get_name()
        update_product_form.price.data = product.get_price()
        update_product_form.description.data = product.get_description()
        update_product_form.tags.data = product.get_tags()

        return render_template('updateProduct.html', form=update_product_form)


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('product_management'))


# Product checkout
@app.route('/checkout2', methods=['GET', 'POST'])
# accepts both get and post methods, checkout page is retrieved
# when form is received, data will be posted onto the server
def purchase():
    create_checkout_form2 = CreateCheckoutForm2(request.form)  # class object, calls server and passes in request
    # Supposed to retrieve the 'amount' parameter from products, I just leave it as 50 for now
    default_amount = 50
    create_checkout_form2.amount.data = default_amount

    if request.method == 'POST' and create_checkout_form2.validate():
        purchases_dict = {}
        db = shelve.open('purchase.db', 'c')

        try:
            purchases_dict = db['Purchases']
        except:
            print("Error in retrieving Purchases from purchase.db.")

        purchase = Purchase.Purchase(create_checkout_form2.fname.data, create_checkout_form2.lname.data,
                                     create_checkout_form2.phone.data, create_checkout_form2.email.data,
                                     create_checkout_form2.add1.data, create_checkout_form2.add2.data,
                                     create_checkout_form2.pcode.data, create_checkout_form2.dmethod.data,
                                     create_checkout_form2.amount.data)
        purchases_dict[purchase.get_purchase_id()] = purchase

        db['Purchases'] = purchases_dict

        db.close()

        return redirect(url_for('success2'))

    return render_template('checkout2.html', form=create_checkout_form2)


@app.route('/purchaseManagement')
def purchase_management():
    purchases_dict = {}
    db = shelve.open('purchase.db', 'r')
    purchases_dict = db['Purchases']
    db.close()

    purchases_list = []
    for key in purchases_dict:
        purchase = purchases_dict.get(key)
        purchases_list.append(purchase)

    return render_template('purchaseManagement.html', count=len(purchases_list), purchases_list=purchases_list)


@app.route('/updatePurchase/<int:id>/', methods=['GET', 'POST'])
def update_purchase(id):
    update_checkout_form2 = CreateUpdateForm2(request.form)
    if request.method == 'POST' and update_checkout_form2.validate():
        purchases_dict = {}
        db = shelve.open('purchase.db', 'w')
        purchases_dict = db['Purchases']

        purchase = purchases_dict.get(id)
        purchase.set_fname(update_checkout_form2.fname.data)
        purchase.set_lname(update_checkout_form2.lname.data)
        purchase.set_phone(update_checkout_form2.phone.data)
        purchase.set_email(update_checkout_form2.email.data)
        purchase.set_add1(update_checkout_form2.add1.data)
        purchase.set_add2(update_checkout_form2.add2.data)
        purchase.set_pcode(update_checkout_form2.pcode.data)
        purchase.set_dmethod(update_checkout_form2.dmethod.data)

        db['Purchases'] = purchases_dict
        db.close()

        return redirect(url_for('purchase_management'))
    else:
        purchases_dict = {}
        db = shelve.open('purchase.db', 'r')
        purchases_dict = db['Purchases']
        db.close()

        purchase = purchases_dict.get(id)
        update_checkout_form2.fname.data = purchase.get_fname()
        update_checkout_form2.lname.data = purchase.get_lname()
        update_checkout_form2.phone.data = purchase.get_phone()
        update_checkout_form2.email.data = purchase.get_email()
        update_checkout_form2.add1.data = purchase.get_add1()
        update_checkout_form2.add2.data = purchase.get_add2()
        update_checkout_form2.pcode.data = purchase.get_pcode()
        update_checkout_form2.dmethod.data = purchase.get_dmethod()

    return render_template('updatePurchase.html', form=update_checkout_form2)


@app.route('/deletePurchase/<int:id>', methods=['POST'])
def delete_purchase(id):
    purchases_dict = {}
    db = shelve.open('purchase.db', 'w')
    purchases_dict = db['Purchases']

    purchases_dict.pop(id)

    db['Purchases'] = purchases_dict
    db.close()

    return redirect(url_for('purchase_management'))


if __name__ == '__main__':
    create_app()
