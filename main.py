from flask import Blueprint
from app import app
from app import db


# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
