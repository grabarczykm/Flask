from datetime import datetime
from flask import current_app
from app2 import db, login_manager #app2 jest nazwą całego modułu || wywołując moduł importujemy z pliku __main__
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #moduł zainstalowany razem z Flaskiem

#Wymagane do login_manager, pozwala odszukać odpowiedniego użytkownika po ID. Połączone z UserMIxin, z class User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): # tworzenie klasy użytkowniak w oparciu o model bazy danych z SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy = True) #powiązanie z klasą Post, backref - dodanie kolumny do klasy Post, atrybut lazy pozwala pobrać dane z klasy Post do danego użytkownika

#Tworzenie tokenów uwierzytelnienie użytkownika
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')#zwracanie tokenu wygenerowanego Serilizerem

    @staticmethod #metoda nie będzie oczekiwała argumentu self
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']#Jeżeli token nie wygasł uzyskujemy ID użytkownika
        except:
            return None

        return User.query.get(user_id)# zwrócenie użytkownika z DB na podstawie pobranego z tokena ID

    def __repr__(self): #
        return(f"User('{self.username}','{self.email}','(self.image_file)')")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):  #
        return (f"Post('{self.title}','{self.date_posted}')")
