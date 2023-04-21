from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize the Flask application
app = Flask(__name__)

# Load the configuration from the Config class
app.config.from_object(Config)

# Initialize the database and migration engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import the views module to register the routes
from app import views
