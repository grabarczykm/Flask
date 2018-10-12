from flask import  Flask
from flask import render_template
from flask import request, redirect, url_for, flash

app = Flask(__name__)

#konfiguracja aplikacji

app.config.update(dict(
    SECRET_KEY = 'bardzosekretnawartosc',
))

# lista pytań
DANE = [{
    'pytanie':'Stolica Hiszpanii to:', # pytanie
    'odpowiedzi': ['Madryt', ' Warszawa', ' Barcelona'], # możliwe odpowiedzi
    'odpok':'Madryt'}, # poprawna odpowiedź
    {
    'pytanie':'Objętosć sześcianu o boku 6cm, wynosi:',
    'odpowiedzi': ['36', '216', '18'],
    'odpok':'216'}
]


@app.route('/', methods = ['GET', 'POST']) #dekorator odnoszący się do adresu głównego
def index(): #widok, czyli funkcja wywoływana przez adres główny

    if request.method == 'POST':
        punkty = 0
        odpowiedzi = request.form

        for pnr, odp in odpowiedzi.items():
            if odp == DANE[int(pnr)]['odpok']:
                punkty += 1

        flash('Liczba poprawnych odpowiedzi to: {0}'.format(punkty))
        return redirect(url_for('index'))

    return render_template('index.html', pytania = DANE) #funkcja do renderowania szablonu, jako argument przyjmuje nazwę pliku szablonu

if __name__ == '__main__':
    app.run(debug = True)