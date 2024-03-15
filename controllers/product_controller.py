from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from init import db
from models.product import Product, product_schema, products_schema
from controllers.customer_controller import is_user_admin

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/')
def get_all_products():
    stmt = db.select(Product).order_by(Product.id.asc())
    products = db.session.scalars(stmt)
    return products_schema.dump(products)


@products_bp.route('/<int:product_id>')
def get_one_product(product_id):
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    return product_schema.dump(product)


@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    body_data = product_schema.load(request.get_json())
    product = Product(
        name=body_data.get('name'),
        price=body_data.get('price'),
        stock=body_data.get('stock')
    )
    db.session.add(product)
    db.session.commit()
    return product_schema.dump(product), 201


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'must be admin to delete product'}, 403
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': 'product successfully deleted'}
    else:
        return {'error': f'product with id {product_id} not found'}, 404


@products_bp.route('/<int:product_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_product(product_id):
    is_admin = is_user_admin()
    if not is_admin:
        return {'error': 'must be admin to edit product details'}
    body_data = product_schema.load(request.get_json(), partial=True)
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        product.name = body_data.get('name') or product.name
        product.price = body_data.get('price') or product.price
        product.stock = body_data.get('stock') or product.stock

        db.session.commit()
        return product_schema.dump(product)
    else:
        return {'error': f'product with if {product_id} not found'}, 404
