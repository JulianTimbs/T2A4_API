from init import db, ma


class Interaction(db.Model):
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True)
    int_type = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)

    user = db.relationship('User', back_populates='interactions')
    customer = db.relationship('Customer', back_populates='interactions')


class InteractionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'int_type', 'date', 'user_id', 'customer_id')
        ordered = True


interaction_schema = InteractionSchema()
interactions_schema = InteractionSchema(many=True)
