from flask import Flask, request, jsonify, render_template, url_for,flash, redirect
from forms import RegistrationForm, LoginForm
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e05201e52103ae9e0b478dc038802df6'

posts = [
    {
        'author': 'moshe',
        'title': 'moshe adventure',
        'content': 'everyone',
        'date': '2/1/2009'
    },
    {
        'author': 'dudu',
        'title': 'dudu adventure',
        'content': 'friends',
        'date': '2/2/2022'
    }
]


@app.route("/")
def print():
    return "<h1>hello<h1>"


@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['Get', 'Post'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['Get', 'Post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You Logged In!!!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unseccessful. Please Try Again', 'danger')
    return render_template('login.html', title='Login', form=form)


# Define a sample route to return a list of items
@app.route('/drinks', methods=['GET'])
def get_items():
    items = jsonify({"drinks": [{"description": "good 1", "name": "apple"}, {"description": "good 2", "name": "orange"},
                                {"description": "good 3", "name": "grapes"}]})
    return items


# Define a route to add a new item
@app.route('/items', methods=['POST'])
def add_item():
    item = request.json['item']
    # Here you could add the new item to a database or some other data store
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
