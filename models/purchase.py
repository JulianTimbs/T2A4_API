from init import db, ma


class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Integer, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)

    product = db.relationship('Product', back_populates='purchases')
    customer = db.relationship('Customer', back_populates='purchases')


class PurchaseSchema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'amount', 'product_id', 'customer_id')
        ordered = True


purchase_schema = PurchaseSchema()
purchases_schema = PurchaseSchema(many=True)
