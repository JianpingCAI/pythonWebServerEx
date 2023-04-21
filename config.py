# This file contains the configuration for the application.
import os


class Config(object):
    # SQL Alchemy configuration
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///regression_testing_system.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

    # Sentry configuration
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
