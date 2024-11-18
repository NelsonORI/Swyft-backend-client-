import os 
from flask import Flask, request, make_response,jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import request, session, make_response
from flask_bcrypt import Bcrypt 
from flask_cors import CORS 

app = Flask(__name__)
app.secret_key = os.environ.get(' USER')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///swyft.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy()
migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)

api = Api(app)