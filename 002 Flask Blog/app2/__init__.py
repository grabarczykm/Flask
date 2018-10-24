from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app2.config import Config #zmienne konfiguracji przerzucone do jednego pliku

db = SQLAlchemy() #stworzenie instancji SQLAlchemy
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' #powiązany z login_required w pliku routes
login_manager.login_message_category = 'info' #informacja o wygladzie wyswietlanych wiadomosci przez login_manager. Przypisanie klasy z bootstrapa 'info'

mail = Mail()


#funkcja odpowiadająca za stworzenie aplikacji
def create_app(config_class = Config):
    app = Flask(__name__) #Stworzenie aplikacji
    app.config.from_object(Config)  # pobranie danych konfiguracyjnych z klasy Config

    #Inicjalizacja modułów zewnetrznych, wykorzystywanych w aplikacji
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app2.users.routes import users  # nazwa instancji Blueprint w module users
    app.register_blueprint(users)  # rejestracja instancji blueprint

    from app2.posts.routes import posts  # nazwa instancji Blueprint w module users
    app.register_blueprint(posts)  # rejestracja instancji blueprint

    from app2.main.routes import main  # nazwa instancji Blueprint w module users
    app.register_blueprint(main)  # rejestracja instancji blueprint

    from app2.errors.handlers import errors
    app.register_blueprint(errors)

    return app