import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Get base directory
base_dir = os.path.abspath(os.path.dirname(__file__))
base_url = '' # Base url

app = Flask(__name__)

# CONFIG
app.config['SECRET_KEY'] = '$tfx37h5kqv*!$4hMfHAvrfEZQFyz0e4r6$49$t3-i0(uN1uwSBQKh!y%6HVnw4n'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + os.path.join(base_dir, "database/data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

OPENWEATHER_API_KEY = "01d414111208781957ed74b5cd09289c"
NEWS_API_KEY = "71487f82-d68e-44f2-b018-2a71aca2188e"
# Create the SqlAlchemy db instance
db = SQLAlchemy(app)