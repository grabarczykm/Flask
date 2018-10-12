from flask import render_template, url_for, flash, redirect
from app2.forms import RegistrationForm, LoginForm
from app2 import app
from app2.models import User, Post


posts = [
    {
        'author':'Piotr Łakomiec',
        'title': 'FrioArte',
        'content':'First post content',
        'date_posted':'April 20,2018'
    },
{
        'author':'Marcin Grabarczyk',
        'title': 'Post number 2 ',
        'content':'Second post content',
        'date_posted':'April 21,2018'
    },
{
        'author':'Chuck Noris',
        'title': 'War in Wietnam',
        'content':'War war war',
        'date_posted':'April 20,1956'
    }
]

@app.route("/")
@app.route("/home")
def home():

    return render_template("home.html", posts=posts)


@app.route("/about")
def about():

    return render_template("about.html", title='About')

@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()#stworzenie instancji formularze na podstawie stworzonego formularze rejestracji

    if form.validate_on_submit():#czy formularz został zvalidowany podczas przesyłania(submit)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()#stworzenie instancji formularze na podstawie stworzonego formularza logowania

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password','danger')

    return render_template('login.html', title='Login', form=form)
