from init import db, ma


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    purchases = db.relationship('Purchase', back_populates='product')


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'stock', 'purchases')
        ordered = True


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
