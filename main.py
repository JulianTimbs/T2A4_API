import os

from flask import Flask

from init import db, ma, bcrypt, jwt


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    # configs
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # connect libraries with flask app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from controllers.cli_controller import db_commands
    app.register_blueprint(db_commands)

    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp)

    from controllers.customer_controller import customer_bp
    app.register_blueprint(customer_bp)

    from controllers.interaction_controller import interaction_bp
    app.register_blueprint(interaction_bp)

    from controllers.product_controller import products_bp
    app.register_blueprint(products_bp)

    from controllers.purchase_controller import purchase_bp
    app.register_blueprint(purchase_bp)

    return app
