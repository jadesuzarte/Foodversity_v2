import requests
from flask import Flask, render_template, url_for, request, redirect, jsonify, current_app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from app import app, db

# def get_db():
#     if 'db' not in g:
#         g.db = sqlite.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite.Row

    # return g.db

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app) #initialized the database

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % self.id #EXPLAIN THIS
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable = False)
    image = db.Column(db.String())
    ingredients = db.Column(db.String())
    ready_in_mins = db.Column(db.Integer)
    dairy = db.Column(db.Boolean)
    vegan = db.Column(db.Boolean)
    gluten_free = db.Column(db.Boolean)
    dairy_free = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    
    def __init__(self, recipe_id, name, image, ingredients, ready_in_mins, dairy, vegan, gluten_free, dairy_free, user_id):
        self.recipe_id = recipe_id
        self.name = name
        self.image = image
        self.ingredients = ingredients
        self.ready_in_mins = ready_in_mins
        self.dairy = dairy
        self.vegan = vegan
        self.gluten_free = gluten_free
        self.dairy_free = dairy_free
        self.user_id = user_id

    def __repr__(self):
        return "%r" % self.recipe_id 

@app.route('/signup', methods=['POST', 'GET'])
def signup_page():
    add = text('INSERT INTO users (username, password) VALUES (?, ?)')
    selecting = text('SELECT id FROM users WHERE username = ?')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        # new_user = Users(username = user_input,password = password_input)
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.engine.execute(add, (username)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
            db.engine.execute(
            )
            db.commit()
            return render_template('registered.html')
        
        flash(error)

    return render_template('signup.html')

        # if error is None:
        #     try:
        #         db.session.add(new_user)
        #         db.session.commit()
        #         return render_template('registered.html')
        #     except:
        #         return "There was a problem with your registration. Please try again later."
        # else:
        #     return render_template ('signup.html')

# API CALLS
@app.route("/")
def homepage():
    return render_template('homepage.html')
        flash(error)
    return render_template('signup.html')

# Goes to a page that displays all recipes (based on the ingredients by the user)
@app.route('/recipe_list', methods=["GET"])
def recipe_list():
    return render_template("recipe_list.html")

# Shows more detail about a chosen recipe
@app.route('/single/<int:id>', methods=["GET"])
def single(id):
    api_key = os.getenv("apikey")
    # Requests to get additional info about the selected recipe and its ingredients
    request_1 = "https://api.spoonacular.com/recipes/{id}/information?apiKey={apikey}&includeNutrition=false&includeInstruction=true".format(id=id, apikey=api_key)
    request_2 = "https://api.spoonacular.com/recipes/{id}/ingredientWidget.json?apiKey={apikey}".format(id=id, apikey=api_key)
    # Sending the requests
    response_1 = requests.get(request_1)
    response_2 = requests.get(request_2)
    # The single recipe and its ingredients
    res_data_1 = response_1.json()
    res_data_2 = response_2.json()
    return render_template("single_recipe.html", recipe=res_data_1, ingredients=res_data_2["ingredients"])

# Shows 8 possible recipes that can be made (given the ingredients)
@app.route('/get_recipes', methods=["GET"])
def get_recipes():
    ingredients = request.args.get('ingredients')
    # Converting the search term into a format that's appropriate for the API call
    search = ','.join(ingredients.split(", "))
    # My spoonacular api key
    api_key = os.getenv("apikey")
    # The http request to the spooner API
    req = "https://api.spoonacular.com/recipes/findByIngredients?apiKey={apikey}&ingredients={ingredients}&number=8".format(apikey=api_key, ingredients=ingredients)
    # Sending the request to the API
    response = requests.get(req)
    # The list of recipes
    res_data = response.json()
    return render_template('recipe_list.html', recipes=res_data)
