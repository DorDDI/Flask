from flask import render_template, request, Blueprint,current_app, flash, redirect, url_for
from app.models import Post
from movies import Movie
from flask_login import login_required
from app.movie_section.movies_forms import SearchForm, UpcomingForm

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


@movie_main.route("/movie_search", methods=['Get', 'Post'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        current_app.config['RES'] = current_app.config['MOVIE'].search(form.search_name.data)
        res = current_app.config['RES']
        number_of_options = int(res['result_count'])
        if number_of_options == 0:
            flash("No movies or TV series found", 'warning')
            return redirect(url_for('movie_main.search'))
        return render_template('movie_search_results.html', title='Movie Search Results',
                               movies=res['results'], form=form, section=current_app.config['SECTION'])
    return render_template('movie_search.html', title='Movie Search',legend='Name of movie or TV seria', form=form,
                           section=current_app.config['SECTION'])


@movie_main.route("/movie_search/<string:number>")
@login_required
def choose(number):
    if len(number) < 9:
        choose_number = int(number)
        res = current_app.config['RES']
        res = current_app.config['MOVIE'].get_by_id(res['results'][choose_number]['id'])
    else:
        res = current_app.config['MOVIE'].get_by_id(number)

    search_type = res.split("\"@type\":")[1].split(",")[0].replace('"', "")
    if search_type == "Movie":
        info = current_app.config['MOVIE'].movie_option(res)
    elif search_type == "PodcastEpisode":
        info = current_app.config['MOVIE'].podcast(res)
        search_type = "Podcast"
    else:
        search_type = 'TV Seria'
        info = current_app.config['MOVIE'].tv_option(res)
    return render_template('movie_result_disp.html', poster=info['Poster'], title='Results', info=info,
                           search_type=search_type, section=current_app.config['SECTION'])


@movie_main.route("/movie_upcoming", methods=['Get', 'Post'])
@login_required
def upcoming():
    form = UpcomingForm()
    if form.validate_on_submit():
        current_app.config['RES'] = current_app.config['MOVIE'].upcoming(form.number_of_movies.data)
        res = current_app.config['RES']
        dates = res.keys()

        return render_template('movie_upcoming_results.html', title='Movie Upcoming Results',
                               movies=res, dates=dates, form=form, section=current_app.config['SECTION'])
    return render_template('movie_upcoming.html', title='Movie Search', legend='Choose number of movies to show',
                           form=form, section=current_app.config['SECTION'])

