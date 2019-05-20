import jwt
import datetime
from flask import request, jsonify, make_response

from config import *
from functions import *

# Import all models and tables
import model

# Import routes
import routes

# If the database is not create
db.create_all()

if __name__ == '__main__':
    app.run("0.0.0.0", 5000)