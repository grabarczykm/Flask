from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

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

class LoginForm(FlaskForm):
    email = SubmitField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')
