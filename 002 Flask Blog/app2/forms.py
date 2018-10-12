""" Place for forms """
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField #importowanie klas pól do formualrza
from wtforms.validators import DataRequired, Length, Email, EqualTo #importowanie klas validatorów ||
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

#Formularz logowania
class LoginForm(FlaskForm):

    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') #pole przesyłające dane z całego formularza