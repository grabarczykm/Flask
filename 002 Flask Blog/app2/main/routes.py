from flask import render_template, request, Blueprint
from app2.models import Post

main = Blueprint('main', __name__)

@main.route("/")#nazwa dekoratora jest taka sama jak nazwa Blueprint
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int) #Pobieranie numeru strony
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #wszystkie posty
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title='About')

