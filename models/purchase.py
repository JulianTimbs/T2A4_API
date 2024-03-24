from marshmallow import fields

from init import db, ma

purchase_product_join = db.Table('purchase_product_join', db.Column('purchase_id', db.Integer, db.ForeignKey(
    'purchases.id')), db.Column('product_id', db.Integer, db.ForeignKey('products.id')))


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer, nullable=False)

    products = db.Column(db.ARRAY(db.Integer), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)

    product = db.relationship(
        'Product', secondary=purchase_product_join, back_populates='purchases')
    customer = db.relationship('Customer', back_populates='purchases')


class PurchaseSchema(ma.Schema):

    class Meta:
        fields = ('id', 'date', 'amount', 'products', 'customer_id')
        ordered = True


purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
