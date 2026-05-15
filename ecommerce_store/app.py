from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- PRODUCT MODEL ----------------

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    price = db.Column(db.Integer)

    description = db.Column(db.String(300))

    image = db.Column(db.String(100))


# ---------------- CREATE DATABASE ----------------

with app.app_context():

    db.create_all()

    # ADD PRODUCTS ONLY ONCE

    if Product.query.count() == 0:

        products = [

            Product(
                name='Rice Bag',
                price=1200,
                description='Premium quality rice 25kg',
                image='rice.jpg'
            ),

            Product(
                name='Sunflower Oil',
                price=250,
                description='1 litre cooking oil',
                image='oil.jpg'
            ),

            Product(
                name='Biscuits Pack',
                price=50,
                description='Chocolate cream biscuits',
                image='biscuits.jpg'
            ),

            Product(
                name='Bath Soap',
                price=40,
                description='Fresh fragrance soap',
                image='soap.jpg'
            )

        ]

        db.session.bulk_save_objects(products)

        db.session.commit()


# ---------------- HOME PAGE ----------------

@app.route('/')
def home():

    products = Product.query.all()

    return render_template(
        'home.html',
        products=products
    )


# ---------------- ADD TO CART ----------------

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):

    cart = session.get('cart', [])

    cart.append(id)

    session['cart'] = cart

    return redirect(url_for('home'))


# ---------------- CART PAGE ----------------

@app.route('/cart')
def cart():

    cart = session.get('cart', [])

    products = []

    total = 0

    for product_id in cart:

        product = Product.query.get(product_id)

        if product:

            products.append(product)

            total += product.price

    return render_template(
        'cart.html',
        products=products,
        total=total
    )


# ---------------- REMOVE ITEM ----------------

@app.route('/remove/<int:id>')
def remove(id):

    cart = session.get('cart', [])

    if id in cart:

        cart.remove(id)

    session['cart'] = cart

    return redirect(url_for('cart'))


# ---------------- RUN ----------------

if __name__ == '__main__':

    app.run(debug=True)