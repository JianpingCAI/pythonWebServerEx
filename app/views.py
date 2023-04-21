# This file contains the views for the application and the API.
# The API is defined using Flask-RESTX.
# The API is defined in the api_blueprint variable.
# The API is registered in the app object in the app/__init__.py file.

from app.models import Project, TestSuite, TestCase, TestRun, TestResult
from app import db # This is the db object from app/__init__.py
from app import app # This is the app object from app/__init__.py
from flask_restx import Namespace, Resource, fields, reqparse, Api
from flask import Blueprint

# Create the API blueprint
api_blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(
    api_blueprint,
    version="1.0",
    title="Regression Testing System API",
    description="A RESTful API for a regression testing system",
)
app.register_blueprint(api_blueprint)


# Define the request parsers
testProject_parser = reqparse.RequestParser()
testProject_parser.add_argument("name", type=str, required=True)
testProject_parser.add_argument("description", type=str, required=False)

testSuite_parser = reqparse.RequestParser()
testSuite_parser.add_argument("name", type=str, required=True)
testSuite_parser.add_argument("description", type=str, required=False)

testCase_parser = reqparse.RequestParser()
testCase_parser.add_argument("name", type=str, required=True)
testCase_parser.add_argument("description", type=str, required=False)

testRun_parser = reqparse.RequestParser()
testRun_parser.add_argument("name", type=str, required=True)
testRun_parser.add_argument("description", type=str, required=False)

testResult_parser = reqparse.RequestParser()
testResult_parser.add_argument("status", type=str, required=True)
testResult_parser.add_argument("output", type=str, required=False)


# Create namespaces
ns_testProject = Namespace("projects", description="Projects operations")
ns_testSuite = Namespace("test_suites", description="Test suites operations")
ns_testCase = Namespace("test_cases", description="Test cases operations")
ns_testRun = Namespace("test_runs", description="Test runs operations")
ns_testResult = Namespace("test_results", description="Test results operations")

# Defin the models
testProject_model = ns_testProject.model(
    "Project",
    {
        "id": fields.Integer(
            required=True, description="The project unique identifier"
        ),
        "name": fields.String(required=True, description="The project name"),
        "description": fields.String(
            required=True, description="The project description"
        ),
    },
)

testSuite_model = ns_testSuite.model(
    "TestSuite",
    {
        "id": fields.Integer(required=True, description="The test suite ID"),
        "name": fields.String(required=True, description="The test suite name"),
        "description": fields.String(description="The test suite description"),
    },
)

testCase_model = ns_testCase.model(
    "TestCase",
    {
        "id": fields.Integer(required=True, description="The test case ID"),
        "name": fields.String(required=True, description="The test case name"),
        "description": fields.String(description="The test case description"),
    },
)

testRun_model = ns_testRun.model(
    "TestRun",
    {
        "id": fields.Integer(required=True, description="The test run ID"),
        "start_time": fields.DateTime(
            dt_format="iso8601", description="The test run start time"
        ),
        "end_time": fields.DateTime(
            dt_format="iso8601", description="The test run end time"
        ),
    },
)

testResult_model = ns_testResult.model(
    "TestResult",
    {
        "id": fields.Integer(required=True, description="The test result ID"),
        "status": fields.String(
            required=True,
            description="The test result status",
            enum=["passed", "failed", "skipped"],
        ),
        "message": fields.String(description="The test result message"),
        "traceback": fields.String(description="The test result traceback"),
    },
)


@ns_testProject.route("/<int:project_id>")
@ns_testProject.param("project_id", "The project identifier")
class ProjectResource(Resource):
    @ns_testProject.doc("get_project")
    @ns_testProject.marshal_with(testProject_model)
    def get(self, project_id):
        project = Project.query.get_or_404(project_id)
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
        }

    @ns_testProject.doc("update_project")
    @ns_testProject.expect(testProject_model)
    @ns_testProject.marshal_with(testProject_model)
    def put(self, project_id):
        args = testProject_parser.parse_args()
        project = Project.query.get_or_404(project_id)
        project.name = args["name"]
        project.description = args["description"]
        db.session.commit()
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
        }

    @ns_testProject.doc("delete_project")
    @ns_testProject.response(204, "Project deleted")
    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {"result": "Project deleted"}


@ns_testProject.route("/")
class ProjectListResource(Resource):
    @ns_testProject.doc("list_projects")
    @ns_testProject.marshal_list_with(testProject_model)
    def get(self):
        projects = Project.query.all()
        return [
            {"id": project.id, "name": project.name, "description": project.description}
            for project in projects
        ]

    @ns_testProject.doc("create_project")
    @ns_testProject.expect(testProject_model)
    @ns_testProject.marshal_with(testProject_model, code=201)
    def post(self):
        args = testProject_parser.parse_args()
        project = Project(name=args["name"], description=args["description"])
        db.session.add(project)
        db.session.commit()
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
        }


@ns_testSuite.route("/<int:project_id>/<int:suite_id>")
@ns_testSuite.param("project_id", "The project identifier")
@ns_testSuite.param("suite_id", "The test suite identifier")
class TestSuiteResource(Resource):
    @ns_testSuite.doc("get_test_suite")
    @ns_testSuite.marshal_with(testSuite_model)
    def get(self, project_id, suite_id):
        test_suite = TestSuite.query.get_or_404(suite_id)
        if test_suite.project_id != project_id:
            return {"error": "Test suite not found in the specified project"}, 404
        return {
            "id": test_suite.id,
            "name": test_suite.name,
            "description": test_suite.description,
        }

    @ns_testSuite.doc("update_test_suite")
    @ns_testSuite.expect(testSuite_model)
    @ns_testSuite.marshal_with(testSuite_model)
    def put(self, project_id, suite_id):
        args = testSuite_parser.parse_args()
        test_suite = TestSuite.query.get_or_404(suite_id)
        if test_suite.project_id != project_id:
            return {"error": "Test suite not found in the specified project"}, 404
        test_suite.name = args["name"]
        test_suite.description = args["description"]
        db.session.commit()
        return {
            "id": test_suite.id,
            "name": test_suite.name,
            "description": test_suite.description,
        }

    @ns_testSuite.doc("delete_test_suite")
    @ns_testSuite.response(204, "Test suite deleted")
    def delete(self, project_id, suite_id):
        test_suite = TestSuite.query.get_or_404(suite_id)
        if test_suite.project_id != project_id:
            return {"error": "Test suite not found in the specified project"}, 404
        db.session.delete(test_suite)
        db.session.commit()
        return {"result": "Test suite deleted"}


@ns_testSuite.route("/<int:project_id>")
@ns_testSuite.param("project_id", "The project identifier")
class TestSuiteListResource(Resource):
    @ns_testSuite.doc("get_test_suites")
    @ns_testSuite.marshal_list_with(testSuite_model)
    def get(self, project_id):
        test_suites = TestSuite.query.filter_by(project_id=project_id).all()
        return [
            {
                "id": test_suite.id,
                "name": test_suite.name,
                "description": test_suite.description,
            }
            for test_suite in test_suites
        ]

    @ns_testSuite.doc("create_test_suite")
    @ns_testSuite.expect(testSuite_model)
    @ns_testSuite.marshal_with(testSuite_model, code=201)
    def post(self, project_id):
        args = testSuite_parser.parse_args()
        test_suite = TestSuite(
            name=args["name"], description=args["description"], project_id=project_id
        )
        db.session.add(test_suite)
        db.session.commit()
        return {
            "id": test_suite.id,
            "name": test_suite.name,
            "description": test_suite.description,
        }


@ns_testCase.route("/<int:project_id>/<int:suite_id>/<int:case_id>")
@ns_testCase.param("project_id", "The project identifier")
@ns_testCase.param("suite_id", "The test suite identifier")
@ns_testCase.param("case_id", "The test case identifier")
class TestCaseResource(Resource):
    @ns_testCase.doc("get_test_case")
    @ns_testCase.marshal_with(testCase_model)
    def get(self, project_id, suite_id, case_id):
        test_case = TestCase.query.get_or_404(case_id)
        if test_case.test_suite_id != suite_id:
            return {"error": "Test case not found in the specified test suite"}, 404
        return {
            "id": test_case.id,
            "name": test_case.name,
            "description": test_case.description,
        }

    @ns_testCase.doc("update_test_case")
    @ns_testCase.expect(testCase_model)
    @ns_testCase.marshal_with(testCase_model)
    def put(self, project_id, suite_id, case_id):
        args = testCase_parser.parse_args()
        test_case = TestCase.query.get_or_404(case_id)
        if test_case.test_suite_id != suite_id:
            return {"error": "Test case not found in the specified test suite"}, 404
        test_case.name = args["name"]
        test_case.description = args["description"]
        db.session.commit()
        return {
            "id": test_case.id,
            "name": test_case.name,
            "description": test_case.description,
        }

    @ns_testCase.doc("delete_test_case")
    @ns_testCase.response(204, "Test case deleted")
    def delete(self, project_id, suite_id, case_id):
        test_case = TestCase.query.get_or_404(case_id)
        if test_case.test_suite_id != suite_id:
            return {"error": "Test case not found in the specified test suite"}, 404
        db.session.delete(test_case)
        db.session.commit()
        return {"result": "Test case deleted"}


@ns_testCase.route("/<int:project_id>/<int:suite_id>")
@ns_testCase.param("project_id", "The project identifier")
@ns_testCase.param("suite_id", "The test suite identifier")
class TestCaseListResource(Resource):
    @ns_testCase.doc("get_test_cases")
    @ns_testCase.marshal_list_with(testCase_model)
    def get(self, project_id, suite_id):
        test_cases = TestCase.query.filter_by(test_suite_id=suite_id).all()
        return [
            {
                "id": test_case.id,
                "name": test_case.name,
                "description": test_case.description,
            }
            for test_case in test_cases
        ]

    @ns_testCase.doc("create_test_case")
    @ns_testCase.expect(testCase_model)
    @ns_testCase.marshal_with(testCase_model)
    def post(self, project_id, suite_id):
        args = testCase_parser.parse_args()
        test_case = TestCase(
            name=args["name"], description=args["description"], test_suite_id=suite_id
        )
        db.session.add(test_case)
        db.session.commit()
        return {
            "id": test_case.id,
            "name": test_case.name,
            "description": test_case.description,
        }


@ns_testRun.route("/<int:project_id>/<int:suite_id>/<int:run_id>")
@ns_testRun.param("project_id", "The project identifier")
@ns_testRun.param("run_id", "The test run identifier")
class TestRunResource(Resource):
    @ns_testRun.doc("get_test_run")
    @ns_testRun.marshal_with(testRun_model)
    def get(self, project_id, run_id):
        test_run = TestRun.query.get_or_404(run_id)
        if test_run.project_id != project_id:
            return {"error": "Test run not found in the specified project"}, 404
        return {
            "id": test_run.id,
            "name": test_run.name,
            "description": test_run.description,
        }

    @ns_testRun.doc("update_test_run")
    @ns_testRun.expect(testRun_model)
    @ns_testRun.marshal_with(testRun_model)
    def put(self, project_id, run_id):
        args = testRun_parser.parse_args()
        test_run = TestRun.query.get_or_404(run_id)
        if test_run.project_id != project_id:
            return {"error": "Test run not found in the specified project"}, 404
        test_run.name = args["name"]
        test_run.description = args["description"]
        db.session.commit()
        return {
            "id": test_run.id,
            "name": test_run.name,
            "description": test_run.description,
        }

    @ns_testRun.doc("delete_test_run")
    @ns_testRun.response(204, "Test run deleted")
    def delete(self, project_id, run_id):
        test_run = TestRun.query.get_or_404(run_id)
        if test_run.project_id != project_id:
            return {"error": "Test run not found in the specified project"}, 404
        db.session.delete(test_run)
        db.session.commit()
        return {"result": "Test run deleted"}


@ns_testRun.route("/<int:project_id>")
@ns_testRun.param("project_id", "The project identifier")
class TestRunListResource(Resource):
    @ns_testRun.doc("list_test_runs")
    @ns_testRun.marshal_list_with(testRun_model)
    def get(self, project_id):
        test_runs = TestRun.query.filter_by(project_id=project_id).all()
        return [
            {
                "id": test_run.id,
                "name": test_run.name,
                "description": test_run.description,
            }
            for test_run in test_runs
        ]

    @ns_testRun.doc("create_test_run")
    @ns_testRun.expect(testRun_model)
    @ns_testRun.marshal_with(testRun_model)
    def post(self, project_id):
        args = testRun_parser.parse_args()
        test_run = TestRun(
            name=args["name"], description=args["description"], project_id=project_id
        )
        db.session.add(test_run)
        db.session.commit()
        return {
            "id": test_run.id,
            "name": test_run.name,
            "description": test_run.description,
        }


@ns_testResult.route("/<int:result_id>")
@ns_testResult.param("project_id", "The project identifier")
@ns_testResult.param("run_id", "The test run identifier")
@ns_testResult.param("result_id", "The test result identifier")
class TestResultResource(Resource):
    @ns_testResult.doc("get_test_result")
    @ns_testResult.marshal_with(testResult_model)
    def get(self, project_id, run_id, result_id):
        test_result = TestResult.query.get_or_404(result_id)
        if test_result.test_run_id != run_id:
            return {"error": "Test result not found in the specified test run"}, 404
        return {
            "id": test_result.id,
            "status": test_result.status,
            "output": test_result.output,
        }

    @ns_testResult.doc("update_test_result")
    @ns_testResult.expect(testResult_model)
    @ns_testResult.marshal_with(testResult_model)
    def put(self, project_id, run_id, result_id):
        args = testResult_parser.parse_args()
        test_result = TestResult.query.get_or_404(result_id)
        if test_result.test_run_id != run_id:
            return {"error": "Test result not found in the specified test run"}, 404
        test_result.status = args["status"]
        test_result.output = args["output"]
        db.session.commit()
        return {
            "id": test_result.id,
            "status": test_result.status,
            "output": test_result.output,
        }


@ns_testResult.route("/")
@ns_testResult.param("project_id", "The project identifier")
@ns_testResult.param("run_id", "The test run identifier")
class TestResultListResource(Resource):
    @ns_testResult.doc("list_test_results")
    @ns_testResult.marshal_list_with(testResult_model)
    def get(self, project_id, run_id):
        test_results = TestResult.query.filter_by(test_run_id=run_id).all()
        return [
            {
                "id": test_result.id,
                "status": test_result.status,
                "output": test_result.output,
            }
            for test_result in test_results
        ]

    @ns_testResult.doc("create_test_result")
    @ns_testResult.expect(testResult_model)
    @ns_testResult.marshal_with(testResult_model)
    def post(self, project_id, run_id):
        args = testResult_parser.parse_args()
        test_result = TestResult(
            status=args["status"], output=args["output"], test_run_id=run_id
        )
        db.session.add(test_result)
        db.session.commit()
        return {
            "id": test_result.id,
            "status": test_result.status,
            "output": test_result.output,
        }


def initialize_routes(api):
    # Register the namespaces
    api.add_namespace(ns_testProject)
    api.add_namespace(ns_testSuite)
    api.add_namespace(ns_testCase)
    api.add_namespace(ns_testRun)
    api.add_namespace(ns_testResult)

# Register the routes
initialize_routes(api)