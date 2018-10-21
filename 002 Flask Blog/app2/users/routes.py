from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app2 import db, bcrypt
from app2.models import User, Post
from app2.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from app2.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['POST', 'GET']) #nazwa dekoratora jest taka sama jak nazwa Blueprint
def register():
    if current_user.is_authenticated:#wyłączenie strony rejestracji jeżeli użytkownik jest zalogowany
        return redirect(url_for('main.home'))
    form = RegistrationForm()#stworzenie instancji formularze na podstawie stworzonego formularze rejestracji

    if form.validate_on_submit():#czy formularz został zvalidowany podczas przesyłania(submit)

        #Tworzenie użytkownika, zapisywanie w DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')# kodowanie hasła w formie UTD-8
        user = User(username=form.username.data, email=form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are able to log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated: #wyłączenie strony logowania jeżeli użytkownik jest zalogowany
        return redirect(url_for('main.home'))
    form = LoginForm()#stworzenie instancji formularze na podstawie stworzonego formularza logowania

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()# sprawdzanie czy użytkownik o podanym emailu jest w bazie
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data )
            next_page = request.args.get('next') #jeżeli chcemy przejsc do strony wymagajacej logowania w URL przy next zapisany jest adres, do którego chcielismy przejsc. Zapisujemy go w zmiennej
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #Jeżeli istnieje next_page przejscie do adresu z next_page, inaczej przejscie do home
        else:
            flash('Login Unsuccessful. Please check email and password','danger')

    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['POST', 'GET'])
@login_required #dekorator stawiający wymaganie zalogowania się - jeżeli spróbujemy wejsć na ten adres bez logowania, przekieruje do widoku logowania
def account():
    form = UpdateAccountForm()

    #Jeżeli formularz jest przesłany i prawidłowy, zaktualizowanie danych użytkownika
    if form.validate_on_submit():
        if form.picture.data: #jeżeli w formularzu przesyłany jest nowy obrazek
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('users.account'))

    #Jeżeli formularz nie jest przesłany, pola wypełnione są aktualnymi danymi
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#Strona z postami wybranego użytkownika
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) #Pobieranie numeru strony
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5) #wszystkie posty stworzone przez jednego użytkownika, z paginacją i posortowane względem daty dodania
    return render_template("user_posts.html", posts=posts, user=user)


#Strona z zapytaniem o zresetowanie hasła
@users.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:  # wyłączenie strony resetowania hasła jeżeli użytkownik jest zalogowany
        return redirect(url_for('main.home'))

    form = RequestResetForm()

    if form.validate_on_submit(): #Wywołany template po SUBMIT przekierowuje do tego samego route. Sprawdzenie czy został użyty SUBMIT
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email ahs been sent wit hinstructions to rese your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


#Akceptowanie zapytania o reset hasła na podstawie wygenerowanego dla użytkowniak tokenu
@users.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:  # wyłączenie strony resetowania hasła jeżeli użytkownik jest zalogowany
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)#Zwraca użytkownika na podstawie przesłanego tokenu
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():#czy formularz został zvalidowany podczas przesyłania(submit)
        #Tworzenie użytkownika, zapisywanie w DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')# kodowanie hasła w formie UTD-8
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form = form)