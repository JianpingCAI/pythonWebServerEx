from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from models import db
from resources import (ProjectResource, ProjectListResource, TestSuiteResource, TestSuiteListResource,
                       TestCaseResource, TestCaseListResource, TestRunResource, TestRunListResource,
                       TestResultResource, TestResultListResource)

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///regression_testing_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create the database tables
@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)

# Register the resources
api.add_resource(ProjectListResource, '/projects')
api.add_resource(ProjectResource, '/projects/<int:project_id>')

api.add_resource(TestSuiteListResource, '/projects/<int:project_id>/suites')
api.add_resource(TestSuiteResource, '/projects/<int:project_id>/suites/<int:suite_id>')

api.add_resource(TestCaseListResource, '/projects/<int:project_id>/suites/<int:suite_id>/cases')
api.add_resource(TestCaseResource, '/projects/<int:project_id>/suites/<int:suite_id>/cases/<int:case_id>')

api.add_resource(TestRunListResource, '/projects/<int:project_id>/runs')
api.add_resource(TestRunResource, '/projects/<int:project_id>/runs/<int:run_id>')

api.add_resource(TestResultListResource, '/projects/<int:project_id>/runs/<int:run_id>/results')
api.add_resource(TestResultResource, '/projects/<int:project_id>/runs/<int:run_id>/results/<int:result_id>')

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
if __name__ == '__main__':
    app.run(debug=True)
