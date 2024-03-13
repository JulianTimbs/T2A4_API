from datetime import date

from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.customer import Customer
from models.interaction import Interaction
from models.product import Product
from models.purchase import Purchase

db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print('Tables created')


@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print('Tables dropped')


@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            full_name='John Smith',
            email='admin@email.com',
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
            is_admin=True
        ),
        User(
            full_name='Frank Doe',
            email='user1@email.com',
            password=bcrypt.generate_password_hash('123456').decode('utf-8'),
        )
    ]

    customers = [
        Customer(
            full_name='customer one',
            email='customer1@email.com',
            phone=123456,
            business='business1',
            user=users[0]
        ),
        Customer(
            full_name='customer two',
            email='customer2@email.com',
            phone=98765,
            business='business2',
            user=users[1]
        ),
        Customer(
            full_name='customer three',
            email='customer3@email.com',
            phone=432567,
            business='',
            user=users[0]
        )
    ]

    interactions = [
        Interaction(
            int_type='email',
            date=date.today(),
            user=users[0],
            customer=customers[0]
        ),
        Interaction(
            int_type='call',
            date=date.today(),
            user=users[0],
            customer=customers[1]
        ),
        Interaction(
            int_type='email',
            date=date.today(),
            user=users[1],
            customer=customers[2]
        )
    ]

    products = [
        Product(
            name='product1',
            price=5.00,
            stock=15
        ),
        Product(
            name='product2',
            price=2.57,
            stock=7
        ),
        Product(
            name='product3',
            price=15.00,
            stock=0
        )
    ]

    purchases = [
        Purchase(
            product=products[0],
            amount=5,
            customer=customers[0],
            date=date.today()
        ),
        Purchase(
            product=products[1],
            amount=10,
            customer=customers[0],
            date=date.today()
        ),
        Purchase(
            product=products[2],
            amount=2,
            customer=customers[2],
            date=date.today()
        )
    ]

    db.session.add_all(users)
    db.session.add_all(customers)
    db.session.add_all(interactions)
    db.session.add_all(products)
    db.session.add_all(purchases)
    db.session.commit()

    print('Tables seeded')
