from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from receipess_app.config import Config


db = SQLAlchemy()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    #rejestracja routes
    from receipess_app.users.routes import users
    from receipess_app.receipess.routes import receipess
    from receipess_app.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(receipess)
    app.register_blueprint(main)

    return app
