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

    for category in categories:
        print(f"Category: {category.name}, Description: {category.description}")

    for query in queries:
        print(f"Question: {query.text}, Category: {query.category.name}")

    return 'Check the console for data'


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

    return 'Data added successfully!'


if __name__ == '__main__':
    app.run(debug=True)
