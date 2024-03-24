from datetime import date

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.purchase import Purchase, purchase_schema, purchases_schema
from models.product import Product
from controllers.customer_controller import is_user_admin

purchase_bp = Blueprint('PurchaseSchema', __name__, url_prefix='/purchases')


@purchase_bp.route('/')
def get_all_purchases():
    stmt = db.select(Purchase).order_by(Purchase.date.desc())
    purchases = db.session.scalars(stmt)
    return purchases_schema.dump(purchases)


@purchase_bp.route('<int:purchase_id>')
def get_one_purchase(purchase_id):
    stmt = db.select(Purchase).filter_by(id=purchase_id)
    purchase = db.session.scalar(stmt)
    return purchase_schema.dump(purchase)


@purchase_bp.route('/', methods=['POST'])
@jwt_required()
def create_purchase():
    body_data = purchase_schema.load(request.get_json())
    purchase = Purchase(
        date=date.today(),
        amount=body_data.get('amount'),
        products=body_data.get('products'),
        customer_id=body_data.get('customer_id')
    )
    db.session.add(purchase)
    db.session.commit()
    return purchase_schema.dump(purchase), 201


@purchase_bp.route('/<int:purchase_id>', methods=['DELETE'])
@jwt_required()
def delete_purchase(purchase_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'must be admin to delete purchase'}
    stmt = db.select(Purchase).filter_by(id=purchase_id)
    purchase = db.session.scalar(stmt)
    if purchase:
        db.session.delete(purchase)
        db.session.commit()
        return {'message': 'purchase deleted successfully'}
    else:
        return {'error': f'purchase with id {purchase_id} not found'}


@purchase_bp.route('/<int:purchase_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_purchase(purchase_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'must be admin to update purchase'}
    body_data = purchase_schema.load(request.get_json(), partial=True)
    stmt = db.select(Purchase).filter_by(id=purchase_id)
    purchase = db.session.scalar(stmt)
    if purchase:
        purchase.date = body_data.get('date') or purchase.date
        purchase.amount = body_data.get('amount') or purchase.amount
        purchase.products = body_data.get(
            'products') or purchase.product_id
        purchase.customer_id = body_data.get(
            'customer_id') or purchase.customer_id

        db.session.commit()
        return purchase_schema.dump(purchase)
    else:
        return {'error': f'purchase with id {purchase_id} not found'}, 404
