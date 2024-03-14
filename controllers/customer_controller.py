from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.customer import Customer, customer_schema, customers_schema
from models.user import User

customer_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customer_bp.route('/')
def get_all_customers():
    stmt = db.select(Customer).order_by(Customer.full_name.asc())
    customers = db.session.scalars(stmt)
    return customers_schema.dump(customers)


@customer_bp.route('/<int:customer_id>')
def get_one_customer(customer_id):
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    if customer:
        return customer_schema.dump(customer)
    else:
        return {'error', f'Customer with id {customer_id} not found'}, 404


@customer_bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    body_data = customer_schema.load(request.get_json())
    customer = Customer(
        full_name=body_data.get('full_name'),
        email=body_data.get('email'),
        phone=body_data.get('phone'),
        business=body_data.get('business'),
        user_id=get_jwt_identity()
    )
    db.session.add(customer)
    db.session.commit()
    return customer_schema.dump(customer), 201


@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'Not authorised to delete a customer'}, 403
    stmt = db.select(Customer).where(Customer.id == customer_id)
    customer = db.session.scalar(stmt)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return {'message': f'Customer with id {customer_id} deleted successfully'}
    else:
        return {'error': f'Customer with if {customer_id} not found'}, 404


@customer_bp.route('<int:customer_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_customer(customer_id):
    body_data = customer_schema.load(request.get_json(), partial=True)
    stmt = db.select(Customer).filter_by(id=customer_id)
    customer = db.session.scalar(stmt)
    is_admin = is_user_admin()
    if customer:
        if not is_admin:
            return {'error': 'Must be admin to edit customer details'}
        customer.full_name = body_data.get('full_name') or customer.full_name
        customer.email = body_data.get('email') or customer.email
        customer.phone = body_data.get('phone') or customer.phone
        customer.business = body_data.get('business') or customer.business

        db.session.commit()
        return customer_schema.dump(customer)
    else:
        return {'error': f'Customer with id {customer_id} not found'}, 404


def is_user_admin():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    return user.is_admin
