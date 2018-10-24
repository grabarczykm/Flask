import os

class Config:
    SECRET_KEY = '809879869sabdyig'  # zabezpiecza aplikację (pliki cookies itd.) przed niepowołaną ingerencją
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # ustawienia konfiguracyjne dla SQL, wskazanie miejsca umiejscowanie bazu danych SQLlite