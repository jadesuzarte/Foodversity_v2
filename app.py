import requests
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app) #initialized the database

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



