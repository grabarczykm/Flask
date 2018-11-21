from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)#instancja bazy danych
migrate = Migrate(app, db) #instancja migratione engine
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'
bcrypt = Bcrypt(app)


from app import routes

