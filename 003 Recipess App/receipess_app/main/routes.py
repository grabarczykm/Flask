from flask import Blueprint

main = Blueprint('main',__name__)

@main.route("/home")
@main.route("/")
def home():
    return ('HOME')