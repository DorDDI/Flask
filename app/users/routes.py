from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app import bcrypt, db
from app.models import Post, User, MusicPost, MovieWatchlist
from flask_login import login_user, current_user, logout_user, login_required
from app.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['Get', 'Post'])
def register():
    if current_user.is_authenticated:
        return redirect((url_for('movie_main.home')))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, section=current_app.config['SECTION'])


@users.route("/login", methods=['Get', 'Post'])
def login():
    if current_user.is_authenticated:
        return redirect((url_for('menu.menu_disp')))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('menu.menu_disp'))
        else:
            flash('Login Unsuccessful. Please Try Again', 'danger')
    return render_template('login.html', title='Login', form=form, section=current_app.config['SECTION'])


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('menu.menu_disp'))


@users.route("/account/<int:section>", methods=['Get', 'Post'])
@login_required
def account(section):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Updated', 'success')
        return redirect(url_for('users.account', section=current_app.config['SECTION']))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form,
                           section=current_app.config['SECTION'])


@users.route("/user/<string:username>/<int:section>")
def user_posts(username, section):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    if section == 1:
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)
        return render_template('movie_user_posts.html', posts=posts, user=user, title='User Posts',
                               section=current_app.config['SECTION'])
    else:
        posts = MusicPost.query.filter_by(author=user).order_by(MusicPost.date_posted.desc())\
            .paginate(page=page, per_page=5)
        return render_template('music_user_posts.html', posts=posts, user=user, title='User Posts',
                               section=current_app.config['SECTION'])


@users.route("/user_watchlist/<string:username>/<int:section>")
def user_watchlist(username, section):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    if section == 1:
        watch = MovieWatchlist.query.filter_by(author=user).order_by(MovieWatchlist.date_posted.desc())\
            .paginate(page=page, per_page=5)
        return render_template('movie_user_watchlist.html', watchs=watch, user=user, title='User Movie Watchlist',
                               section=current_app.config['SECTION'])
    else:
        pass
        # return render_template('music_user_posts.html', watch=watch, user=user, title='User Posts',
        # section=current_app.config['SECTION'])


@users.route("/user/<string:username>")
def user_music_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = MusicPost.query.filter_by(author=user).order_by(MusicPost.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('music_user_posts.html', posts=posts, user=user, title='User Posts')


@users.route("/reset_password", methods=['Get', 'Post'])
def reset_request():
    if current_user.is_authenticated:
        return redirect((url_for('movie_main.home')))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has set to reset password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form, section=current_app.config['SECTION'])


@users.route("/reset_password/<token>", methods=['Get', 'Post'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect((url_for('movie_main.home')))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated', 'success')
        current_app.config['SECTION'] = 0
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form, section=0)
