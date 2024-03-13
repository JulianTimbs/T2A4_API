from init import db, ma
from marshmallow import fields


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # MUST DO RELATIONSHIP TO INTERACTIONS
    customers = db.relationship('Customer', back_populates='user')
    interactions = db.relationship('Interaction', back_populates='user')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'full_name', 'email',
                  'password', 'is_admin', 'customers', 'interactions')


user_schema = UserSchema(exclude=['password', 'customers', 'interactions'])

users_schema = UserSchema(many=True, exclude=['password'])
