from flask import render_template, request, Blueprint,current_app, flash, redirect, url_for,abort
from app.models import Post, MovieWatchlist
from app import db
from flask_login import login_required, current_user
from app.movie_section.movies_forms import SearchForm, UpcomingForm, PopularForm, WatchlistForm

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
    return render_template('movie_search.html', title='Movie Search', legend='Name of movie or TV seria', form=form,
                           section=current_app.config['SECTION'])


@movie_main.route("/movie_search/<string:number>")
@login_required
def choose(number):
    if len(number) < 9:
        choose_number = int(number)
        res = current_app.config['RES']
        id = res['results'][choose_number]['id']
        res = current_app.config['MOVIE'].get_by_id(id)
    else:
        id = number
        res = current_app.config['MOVIE'].get_by_id(id)

    search_type = res.split("\"@type\":")[1].split(",")[0].replace('"', "")
    if search_type == "Movie":
        info = current_app.config['MOVIE'].movie_option(res)
    elif search_type == "PodcastEpisode":
        info = current_app.config['MOVIE'].podcast(res)
        search_type = "Podcast"
    else:
        search_type = 'TV Seria'
        info = current_app.config['MOVIE'].tv_option(res)
    info['ID'] = id
    info['Type Search'] = search_type
    current_app.config['RES'] = info
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


@movie_main.route("/movie_popular/<int:pop_type>/<int:section>", methods=['Get', 'Post'])
@login_required
def popular(pop_type, section):
    form = PopularForm()
    if pop_type == 1:
        str_type = 'Movie'
    else:
        str_type = 'TV Seria'
    if form.validate_on_submit():
        current_app.config['RES'] = current_app.config['MOVIE'].get_popular(pop_type, genre=form.choices.data,
                                                                            start_id=form.start.data,
                                                                            movie_number=form.number_of_movies.data)
        res = current_app.config['RES']
        return render_template('movie_popular_results.html', title='Movie Upcoming Results',
                               movies=res['results'], form=form, section=current_app.config['SECTION'])
    return render_template('movie_popular.html', title='Movie Search', legend=f'Popular {str_type}',
                           form=form, section=current_app.config['SECTION'])


@movie_main.route("/movie_watchlist", methods=['Get', 'Post'])
@login_required
def new_watchlist():
    form = WatchlistForm()
    info = current_app.config['RES']
    watch_option = MovieWatchlist.query.filter_by(author=current_user, id=info['ID']).first()
    if watch_option:
        flash('Your Watchlist Already Added', 'info')
        return redirect(url_for('users.user_watchlist', username=current_user.username,
                                section=current_app.config['SECTION']))
    else:
        if form.validate_on_submit():
            info_keys = info.keys()
            if 'Duration' not in info_keys:
                dur = None
            else:
                dur = info['Duration']
            watchlist_item = MovieWatchlist(id=info['ID'], title=info['Name'], poster=info['Poster'],
                                            type_watch=form.watch_type.data, duration=dur, rate=form.rate.data,
                                            actors=info['Actors'], date_year=info['Year'],
                                            content_rate=info['Content Rate'], genre=info['Genre'], author=current_user)
            db.session.add(watchlist_item)
            db.session.commit()
            flash('Your Watchlist Added', 'success')
            return redirect(url_for('movie_main.home'))
        return render_template('movie_watchlist.html', title='New Watchlist', info=info, form=form,
                               legend='New Watchlist', section=current_app.config['SECTION'])


@movie_main.route("/movie_watchlist/<string:watchlist_id>/update/<int:section>", methods=['Get', 'Post'])
@login_required
def update_watchlist(watchlist_id, section):
    watch = MovieWatchlist.query.get_or_404(watchlist_id)
    info = {'ID': watch.id, 'Name': watch.title, 'Poster': watch.poster, 'Duration': watch.duration,
            'Actors': watch.actors, 'Year': watch.date_year, 'Content Rate': watch.content_rate, 'Genre': watch.genre}
    if watch.author != current_user:
        abort(403)
    form = WatchlistForm()
    if form.validate_on_submit():
        watch.type_watch = form.watch_type.data
        watch.rate = form.rate.data
        db.session.commit()
        flash('Your Watchlist Updated', 'success')
        return redirect(url_for('users.user_watchlist', username=current_user.username,
                                section=current_app.config['SECTION']))
    elif request.method == 'GET':
        form.rate.data = watch.rate
        form.watch_type.data = watch.type_watch
    return render_template('movie_watchlist.html',  title='Update Post', info=info, form=form, legend='Update Post',
                           section=current_app.config['SECTION'])


@movie_main.route("/movie_watchlist/<string:watchlist_id>/delete/<int:section>", methods=['Post'])
@login_required
def delete_post(watchlist_id, section):
    watch = MovieWatchlist.query.get_or_404(watchlist_id)
    if watch.author != current_user:
        abort(403)
    db.session.delete(watch)
    db.session.commit()
    flash('Your Watchlist Deleted', 'success')
    return redirect(url_for('users.user_watchlist', username=current_user.username,
                            section=current_app.config['SECTION']))
