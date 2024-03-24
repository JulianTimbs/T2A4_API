from marshmallow import fields

from init import db, ma
from models.purchase import purchase_product_join


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    purchases = db.relationship(
        'Purchase', secondary=purchase_product_join, back_populates='product')


class ProductSchema(ma.Schema):
    purchases = fields.List(fields.Nested('PurchaseSchema', only=['id']))

    class Meta:
        fields = ('id', 'name', 'price', 'stock', 'purchases')
        ordered = True


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
