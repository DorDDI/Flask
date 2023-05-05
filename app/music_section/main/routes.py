from flask import render_template, request, Blueprint,current_app
from app.models import MusicPost

music_main = Blueprint('music_main', __name__)

@music_main.route("/music_home")
def home():
    page = request.args.get('page', 1, type=int)
    current_app.config['SECTION'] = 2
    posts = MusicPost.query.order_by(MusicPost.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('music_home.html', posts=posts, title='Home', section=current_app.config['SECTION'])


@music_main.route("/music")
def about():
    current_app.config['SECTION'] = 2
    return render_template('about.html', title='About', section=current_app.config['SECTION'])

