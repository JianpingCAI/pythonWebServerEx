from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Initialize the Flask application
app = Flask(__name__)

# Load the configuration from the Config class
app.config.from_object(Config)

# Initialize the database and migration engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Sentry
if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        environment='production',
    )

# Set up logging
if not app.debug:
    # Set up logging to a file
    log_level = logging.getLevelName(Config.LOG_LEVEL)
    file_handler = RotatingFileHandler('regression_testing_system.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(log_level)
    app.logger.addHandler(file_handler)

    # Set up logging to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    console_handler.setLevel(log_level)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(log_level)
    app.logger.info('Regression testing system startup')
    
# Import the views module to register the routes
from app import views

