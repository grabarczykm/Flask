import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '809879869sabdyig' #zabezpiecza aplikację (pliki cookies itd.) przed niepowołaną ingerencją
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #ustawienia konfiguracyjne dla SQL, wskazanie miejsca umiejscowanie bazu danych SQLlite
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


db = SQLAlchemy(app) #stworzenie instancji SQLAlchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login' #powiązany z login_required w pliku routes
login_manager.login_message_category = 'info' #informacja o wygladzie wyswietlanych wiadomosci przez login_manager. Przypisanie klasy z bootstrapa 'info'


from app2.users.routes import users #nazwa instancji Blueprint w module users
app.register_blueprint(users) #rejestracja instancji blueprint

from app2.posts.routes import posts #nazwa instancji Blueprint w module users
app.register_blueprint(posts)#rejestracja instancji blueprint

from app2.main.routes import main #nazwa instancji Blueprint w module users
app.register_blueprint(main)#rejestracja instancji blueprint