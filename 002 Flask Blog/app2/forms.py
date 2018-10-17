""" Place for forms """
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField #importowanie klas pól do formualrza
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError #importowanie klas validatorów ||
from app2.models import User
from flask_login import current_user
# DataRequired - pole nie moze zostać puste

#Formularz rejestracji
class RegistrationForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min = 2, max=20)]) #pierwszy argument to wyświetlana etykieta, drugi to ograniczenia nałożone na wprowadzoną wartosć
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up') #pole przesyłające dane z całego formularza

    #Funkcja służąca validowaniu rejestracji (czy nazwy i mail się nie powtarzają)
    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first() # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()  # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

#Formularz logowania
class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') #pole przesyłające dane z całego formularza

# Aktualizacja konta uzytkownika
class UpdateAccountForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min = 2, max=20)]) #pierwszy argument to wyświetlana etykieta, drugi to ograniczenia nałożone na wprowadzoną wartosć
    email = StringField('Email',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update') #pole przesyłające dane z całego formularza

    #Funkcja służąca formularza aktualizacji
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first() # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

#Tworzenie posta
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
