from flask import Flask, request, jsonify, render_template,url_for
import json

app = Flask(__name__)

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
    return render_template('home.html', posts = posts,  title = 'Home')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')





# Define a sample route to return a list of items
@app.route('/drinks',methods=['GET'])
def get_items():
    items = jsonify({"drinks": [{"description": "good 1", "name": "apple"},{"description": "good 2", "name": "orange"},{"description": "good 3", "name": "grapes"}]})
    return items

# Define a route to add a new item
@app.route('/items', methods=['POST'])
def add_item():
    item = request.json['item']
    # Here you could add the new item to a database or some other data store
    return jsonify({'success': True})



if __name__ == '__main__':
    app.run(debug=True)