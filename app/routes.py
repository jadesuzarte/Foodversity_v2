import os
import requests
import sqlite3
from flask import Flask, render_template, url_for, request, redirect, jsonify, current_app, g, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from app import app, db

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

# API CALLS
@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    error = None

    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        new_user = Users(username=username, password=password)
        existing_or_not_existing = Users.query.filter_by(username=username).first()
            
        if existing_or_not_existing:
            error = "User {} is already registered".format(username)

        if error is None:
            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template("registered.html")
            except:
                return str(sys.exc_info()[1])
        else:
            return render_template("error.html", error=error)

    return redirect("/signup")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None 
    if request.method == "GET":
        return render_template("homepage.html")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        existing_or_not_existing = Users.query.filter_by(username=username, password=password).first()

        if existing_or_not_existing:
            user = Users.query.filter_by(username=username, password=password).first()
            user_id = user.id
            route = '/profile/{}'.format(user_id)
            return redirect(route)
        else: 
            return render_template("error.html", error='User/password is incorrect or do not exist') 
    
    return render_template("user_profile.html")

@app.route('/profile/<int:id>')
def profile(id):
    user = Users.query.filter_by(id=id).first()
    username = user.username
    return render_template("user_profile.html", user_id=id, username=username)

# Goes to a page that displays all recipes on the profile page (based on the ingredients by the user)
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
@app.route('/get_recipes/<int:id>', methods=["GET"])
def get_recipes(id):
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
    return render_template('recipe_list.html', recipes=res_data, user_id=id)

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")