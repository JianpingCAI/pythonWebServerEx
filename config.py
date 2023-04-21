# This file contains the configuration for the application.
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///regression_testing_system.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
