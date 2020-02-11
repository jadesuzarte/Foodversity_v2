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
     content = db.Column(db.String(200), nullable=False)
     date_created = db.Column(db.DateTime, default=datetime.utcnow )

     def __repr__(self):
         return '<Task %r>' % self.id #EXPLAIN THIS
