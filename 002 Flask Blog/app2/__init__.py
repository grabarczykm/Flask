from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '809879869sabdyig' #zabezpiecza aplikację (pliki cookies itd.) przed niepowołaną ingerencją
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #ustawienia konfiguracyjne dla SQL, wskazanie miejsca umiejscowanie bazu danych SQLlite

db = SQLAlchemy(app) #stworzenie instancji SQLAlchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #powiązany z login_required w pliku routes
login_manager.login_message_category = 'info' #informacja o wygladzie wyswietlanych wiadomosci przez login_manager. Przypisanie klasy z bootstrapa 'info'

from app2 import routes