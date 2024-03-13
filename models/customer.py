from init import db, ma
from marshmallow import fields


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    # Can be nullable for a customer that doesn't have a business
    business = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='customers')
    interactions = db.relationship('Interaction', back_populates='customer')


class CustomerSchema(ma.Schema):
    # user = fields.Nested('UserSchema', only=['full_name'])

    class Meta:
        fields = ('id', 'full_name', 'email', 'phone',
                  'business', 'user', 'interactions')
        ordered = True


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
