from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '809879869sabdyig' #zabezpiecza aplikację (pliki cookies itd.) przed niepowołaną ingerencją
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #ustawienia konfiguracyjne dla SQL, wskazanie miejsca umiejscowanie bazu danych SQLlite
db = SQLAlchemy(app) #stworzenie instancji SQLAlchemy

from app2 import routes