from flask import render_template, request, Blueprint,current_app
from app.models import Post

movie_main = Blueprint('movie_main', __name__)

@movie_main.route("/movie_home")
def home():
    page = request.args.get('page', 1, type=int)
    current_app.config['SECTION'] = 1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('movie_home.html', posts=posts, title='Home', section=current_app.config['SECTION'])


@movie_main.route("/movie_about")
def about():
    current_app.config['SECTION'] = 1
    return render_template('about.html', title='About', section=current_app.config['SECTION'])

