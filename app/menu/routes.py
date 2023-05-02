from flask import render_template, current_app, Blueprint
from app.models import Post

menu = Blueprint('menu', __name__)



@menu.route("/")
def manu_disp():
    current_app.config['SECTION'] = 0
    return render_template('menu.html', title='Menu', section=current_app.config['SECTION'])

@menu.route("/main_about")
def main_about():
    current_app.config['SECTION'] = 0
    return render_template('about.html', title='Menu', section=current_app.config['SECTION'])
