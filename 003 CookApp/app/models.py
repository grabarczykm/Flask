from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

#Wykorzystywane przez login_manager do odnajdywania użytkownika po user_id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #nadpisanie klasy UserMixin - zapewnia podstawowe metodt login_manager (is_authenticated, is_active, is_anynomus, get_id)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    receipess = db.relationship('Receipe', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    ingredients = db.relationship('Ingredient', backref='author', lazy=True)


    def __repr__(self):
        return (f"User('{self.username}', '{self.email}', '{self.image_file}')")

Rec_Ing = db.Table('Rec_Ing',
                   db.Column('receipe_id',db.Integer, db.ForeignKey('receipe.id')),
                   db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                   )

class Receipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredients = db.relationship('Ingredient', secondary = Rec_Ing, backref = db.backref('receipess', lazy='dynamic'))
    comments = db.relationship('Comment', backref='receipe', lazy=True)

    def __repr__(self):
        return (f"Receipe('{self.title}', '{self.date_posted}')")

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return (f"Ingredient(' { self.name }')")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receipe_id = db.Column(db.Integer, db.ForeignKey('receipe.id'), nullable=False)

    def __repr__(self):
        return (f"Comment(' { self.author }','{self.receipe}')")







