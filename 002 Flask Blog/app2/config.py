import os

class Config:
    SECRET_KEY = '809879869sabdyig'  # zabezpiecza aplikację (pliki cookies itd.) przed niepowołaną ingerencją
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # ustawienia konfiguracyjne dla SQL, wskazanie miejsca umiejscowanie bazu danych SQLlite
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')