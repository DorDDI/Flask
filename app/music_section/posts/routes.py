from flask import render_template, url_for,flash, redirect, request, abort, Blueprint, current_app
from app.music_section.posts.forms import PostForm
from app import db
from app.models import MusicPost
from flask_login import current_user, login_required


music_posts = Blueprint('music_posts', __name__)


@music_posts.route("/music_post/new/<int:section>", methods=['Get', 'Post'])
@login_required
def new_post(section):
    form = PostForm()
    if form.validate_on_submit():
        music_post = MusicPost(title=form.title.data, content=form.content.data, author= current_user)
        db.session.add(music_post)
        db.session.commit()
        flash('Your Post Created', 'success')
        return redirect(url_for('music_main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', section=current_app.config['SECTION'])

@music_posts.route("/music_post/<int:post_id>/<int:section>")
def post(post_id,section):
    music_post = MusicPost.query.get_or_404(post_id)
    return render_template('post.html', title=music_post.title, post=music_post, section=current_app.config['SECTION'])

@music_posts.route("/music_post/<int:post_id>/update<int:section>", methods=['Get', 'Post'])
@login_required
def update_post(post_id,section):
    music_post = MusicPost.query.get_or_404(post_id)
    if music_post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        music_post.title = form.title.data
        music_post.content = form.content.data
        db.session.commit()
        flash('Your Post Updated', 'success')
        return redirect(url_for('music_posts.post', post_id=post_id, section=current_app.config['SECTION']))
    elif request.method=='GET':
        form.title.data = music_post.title
        form.content.data= music_post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post',section=current_app.config['SECTION'])

@music_posts.route("/music_post/<int:post_id>/delete<int:section>", methods=['Post'])
@login_required
def delete_post(post_id,section):
    music_post = MusicPost.query.get_or_404(post_id)
    if music_post.author != current_user:
        abort(403)
    db.session.delete(music_post)
    db.session.commit()
    flash('Your Post Deleted', 'success')
    return redirect(url_for('music_main.home'))
