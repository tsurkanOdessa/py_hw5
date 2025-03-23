from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from models.category import Category
from models.product import Product
from models.sql_queries import Queries

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():

    categories = Category.query.all()
    queries = Queries.query.all()
    products = Product.query.all()

    for category in categories:
        print(f"Category: {category.name}, Description: {category.description}")

    print_separator()

    for query in queries:
        print(f"Query: {query.text}, Category: {query.category.name}")

    print_separator()

    for product in products:
        print(
            f"Product: {product.name}, Price: {product.price}, In Stock: {product.in_stock}, Category: {product.category.name}")

    return 'Перейдите в консоль что бы проверить данные'


@app.route('/add_data')
def add_data():
    category_electronics = Category(name="Электроника", description="Гаджеты и устройства.")
    category_books = Category(name="Книги", description="Печатные книги и электронные книги.")
    category_clothing = Category(name="Одежда", description="Одежда для мужчин и женщин.")

    db.session.add_all([category_electronics, category_books, category_clothing])
    db.session.commit()

    query1 = Queries(text="Какая модель смартфона самая популярная?",
                         category_id=category_electronics.id)
    query2 = Queries(text="Какие книги будут интересны любителям фантастики?",
                         category_id=category_books.id)

    db.session.add_all([query1, query2])
    db.session.commit()

    product_smartphone = Product(name="Смартфон", price=299.99, in_stock=True, category_id=category_electronics.id)
    product_laptop = Product(name="Ноутбук", price=499.99, in_stock=True, category_id=category_electronics.id)
    product_book = Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=category_books.id)
    product_jeans = Product(name="Джинсы", price=40.50, in_stock=True, category_id=category_clothing.id)
    product_tshirt = Product(name="Футболка", price=20.00, in_stock=True, category_id=category_clothing.id)

    db.session.add_all([product_smartphone, product_laptop, product_book, product_jeans, product_tshirt])
    db.session.commit()

    return 'Все данные успешно добавлены'

def print_separator():
    separator = '_' * 80
    print(separator)


if __name__ == '__main__':
    app.run(debug=True)
