import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app2 import mail

#Zapisywanie obrazka przesłanego w formularzu do bazy danych
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #robicie nazwy załadowanego pliku na nazwę i rozszerzenie, tak aby zapisać obraz w tym samych formacie
    picture_fn = random_hex + f_ext #utworzenie nowej nazwy obrazka na podstawie randomowego tokena i rozszerzenia pliku
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #ścieżka do zapisania nowego pliku

    #Zmiana rozmiaru zdjęcia tutaj zamiast w CSS żeby zaoszczędzić czas i moc na przesyłaniu zdjęć dużej wielkości
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) #zapisanie załadowanego obrazka

    return picture_fn


# Funkcja wysyłająca maila z uwierzytelniającym tokenem na maila
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='fireice93@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link: {url_for('users.reset_token', token=token, _external = True)} 

    If you did not make this request then simply ignore this email'''  # atrybut external spowoduje wygenerowanie całego URL, nie tylko skróconego, odpowiedniego dla linku wewnątrz aplikacji

    mail.send(msg)