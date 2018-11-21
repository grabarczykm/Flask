from app import app, bcrypt, db
from flask import render_template, url_for, flash, redirect
from app.models import User, Receipe
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    receipess = Receipe.query.order_by(Receipe.date_posted)
    return render_template('home.html', receipess=receipess)

@app.route("/login")
def login():

    # Jeżeli użytkownik jest zalogowany
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return  redirect(url_for('home'))
        else:
            flash('Login Unsuccesfull. Please check email adress and password')

    return render_template('login.html', form=form)

@app.route("/register", methods=['POST','GET'])
def register():

    #Jeżeli użytkownik jest zalogowany
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    

    #Jeżeli formularz został wypełniony prawidłowo
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created. You are able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',form=form)
