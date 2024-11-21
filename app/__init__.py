from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import os
import certifi



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://axk68420:JGWE4RdbICzCBjNV@cluster0.x6ffwl7.mongodb.net/parking_management"
app.debug = True
app.secret_key = 'parking'
ca = certifi.where()

mongo = PyMongo(app, tlsCAFile=ca)


