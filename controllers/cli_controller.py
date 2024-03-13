from flask import Blueprint

from init import db, bcrypt
from models.user import User
from models.customer import Customer

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

    db.session.add_all(users)
    db.session.add_all(customers)
    db.session.commit()

    print('Tables seeded')
