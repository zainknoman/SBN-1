from __main__ import app
from flask_pymongo import PyMongo

app.config['SECRET_KEY'] = '65be61ace4c4e656af472288a7202919'
app.config['MONGO_URI'] = "mongodb://localhost:27017/sbndb"



class db():
	mongodb_client = PyMongo(app)
	# app.config["CACHE_TYPE"] = "null" 
	connect = mongodb_client.db
