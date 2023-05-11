from flask import render_template, url_for,flash, redirect, request, abort, Blueprint, current_app
from app.movie_section.posts.forms import PostForm
from app import db
from app.models import Post
from flask_login import current_user, login_required


movie_posts = Blueprint('movie_posts', __name__)


@movie_posts.route("/movie_post/new/<int:section>", methods=['Get', 'Post'])
@login_required
def new_post(section):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post Created', 'success')
        return redirect(url_for('movie_main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', section=current_app.config['SECTION'])

@movie_posts.route("/movie_post/<int:post_id>/<int:section>")
def post(post_id, section):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, section=current_app.config['SECTION'])

@movie_posts.route("/movie_post/<int:post_id>/update/<int:section>", methods=['Get', 'Post'])
@login_required
def update_post(post_id, section):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post Updated', 'success')
        return redirect(url_for('movie_posts.post', post_id=post_id, section=current_app.config['SECTION']))
    elif request.method=='GET':
        form.title.data = post.title
        form.content.data= post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', section=current_app.config['SECTION'])

@movie_posts.route("/movie_post/<int:post_id>/delete<int:section>", methods=['Post'])
@login_required
def delete_post(post_id,section):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Deleted', 'success')
    return redirect(url_for('movie_main.home'))
