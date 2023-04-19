from flask_restful import Resource, reqparse
from models import Project, TestSuite, TestCase, TestRun, TestResult, db

# Define the request parsers
project_parser = reqparse.RequestParser()
project_parser.add_argument('name', type=str, required=True)
project_parser.add_argument('description', type=str, required=False)

test_suite_parser = reqparse.RequestParser()
test_suite_parser.add_argument('name', type=str, required=True)
test_suite_parser.add_argument('description', type=str, required=False)

test_case_parser = reqparse.RequestParser()
test_case_parser.add_argument('name', type=str, required=True)
test_case_parser.add_argument('description', type=str, required=False)

test_run_parser = reqparse.RequestParser()
test_run_parser.add_argument('name', type=str, required=True)
test_run_parser.add_argument('description', type=str, required=False)

test_result_parser = reqparse.RequestParser()
test_result_parser.add_argument('status', type=str, required=True)
test_result_parser.add_argument('output', type=str, required=False)

class ProjectResource(Resource):
    def get(self, project_id):
        project = Project.query.get_or_404(project_id)
        return {'id': project.id, 'name': project.name, 'description': project.description}

    def put(self, project_id):
        args = project_parser.parse_args()
        project = Project.query.get_or_404(project_id)
        project.name = args['name']
        project.description = args['description']
        db.session.commit()
        return {'id': project.id, 'name': project.name, 'description': project.description}

    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {'result': 'Project deleted'}

class ProjectListResource(Resource):
    def get(self):
        projects = Project.query.all()
        return [{'id': project.id, 'name': project.name, 'description': project.description} for project in projects]

    def post(self):
        args = project_parser.parse_args()
        project = Project(name=args['name'], description=args['description'])
        db.session.add(project)
        db.session.commit()
        return {'id': project.id, 'name': project.name, 'description': project.description}

class TestSuiteResource(Resource):
    def get(self, project_id, suite_id):
        test_suite = TestSuite.query.get_or_404(suite_id)
        if test_suite.project_id != project_id:
            return {'error': 'Test suite not found in the specified project'}, 404
        return {'id': test_suite.id, 'name': test_suite.name, 'description': test_suite.description}

    def put(self, project_id, suite_id):
        args = test_suite_parser.parse_args()
        test_suite = TestSuite.query.get_or_404(suite_id)
        if test_suite.project_id != project_id:
            return {'error': 'Test suite not found in the specified project'}, 404
        test_suite.name = args['name']
        test_suite.description = args['description']
        db.session.commit()
        return {'id': test_suite.id, 'name': test_suite.name, 'description': test_suite.description}

    def delete(self, project_id, suite_id):
        test_suite = TestSuite.query.get_or_404(suite_id)
        if test_suite.project_id != project_id:
            return {'error': 'Test suite not found in the specified project'}, 404
        db.session.delete(test_suite)
        db.session.commit()
        return {'result': 'Test suite deleted'}

class TestSuiteListResource(Resource):
    def get(self, project_id):
        test_suites = TestSuite.query.filter_by(project_id=project_id).all()
        return [{'id': test_suite.id, 'name': test_suite.name, 'description': test_suite.description} for test_suite in test_suites]

    def post(self, project_id):
        args = test_suite_parser.parse_args()
        test_suite = TestSuite(name=args['name'], description=args['description'], project_id=project_id)
        db.session.add(test_suite)
        db.session.commit()
        return {'id': test_suite.id, 'name': test_suite.name, 'description': test_suite.description}

class TestCaseResource(Resource):
    def get(self, project_id, suite_id, case_id):
        test_case = TestCase.query.get_or_404(case_id)
        if test_case.test_suite_id != suite_id:
            return {'error': 'Test case not found in the specified test suite'}, 404
        return {'id': test_case.id, 'name': test_case.name, 'description': test_case.description}

    def put(self, project_id, suite_id, case_id):
        args = test_case_parser.parse_args()
        test_case = TestCase.query.get_or_404(case_id)
        if test_case.test_suite_id != suite_id:
            return {'error': 'Test case not found in the specified test suite'}, 404
        test_case.name = args['name']
        test_case.description = args['description']
        db.session.commit()
        return {'id': test_case.id, 'name': test_case.name, 'description': test_case.description}

    def delete(self, project_id, suite_id, case_id):
        test_case = TestCase.query.get_or_404(case_id)
        if test_case.test_suite_id != suite_id:
            return {'error': 'Test case not found in the specified test suite'}, 404
        db.session.delete(test_case)
        db.session.commit()
        return {'result': 'Test case deleted'}

class TestCaseListResource(Resource):
    def get(self, project_id, suite_id):
        test_cases = TestCase.query.filter_by(test_suite_id=suite_id).all()
        return [{'id': test_case.id, 'name': test_case.name, 'description': test_case.description} for test_case in test_cases]

    def post(self, project_id, suite_id):
        args = test_case_parser.parse_args()
        test_case = TestCase(name=args['name'], description=args['description'], test_suite_id=suite_id)
        db.session.add(test_case)
        db.session.commit()
        return {'id': test_case.id, 'name': test_case.name, 'description': test_case.description}

class TestRunResource(Resource):
    def get(self, project_id, run_id):
        test_run = TestRun.query.get_or_404(run_id)
        if test_run.project_id != project_id:
            return {'error': 'Test run not found in the specified project'}, 404
        return {'id': test_run.id, 'name': test_run.name, 'description': test_run.description}

    def put(self, project_id, run_id):
        args = test_run_parser.parse_args()
        test_run = TestRun.query.get_or_404(run_id)
        if test_run.project_id != project_id:
            return {'error': 'Test run not found in the specified project'}, 404
        test_run.name = args['name']
        test_run.description = args['description']
        db.session.commit()
        return {'id': test_run.id, 'name': test_run.name, 'description': test_run.description}

    def delete(self, project_id, run_id):
        test_run = TestRun.query.get_or_404(run_id)
        if test_run.project_id != project_id:
            return {'error': 'Test run not found in the specified project'}, 404
        db.session.delete(test_run)
        db.session.commit()
        return {'result': 'Test run deleted'}

class TestRunListResource(Resource):
    def get(self, project_id):
        test_runs = TestRun.query.filter_by(project_id=project_id).all()
        return [{'id': test_run.id, 'name': test_run.name, 'description': test_run.description} for test_run in test_runs]

    def post(self, project_id):
        args = test_run_parser.parse_args()
        test_run = TestRun(name=args['name'], description=args['description'], project_id=project_id)
        db.session.add(test_run)
        db.session.commit()
        return {'id': test_run.id, 'name': test_run.name, 'description': test_run.description}

class TestResultResource(Resource):
    def get(self, project_id, run_id, result_id):
        test_result = TestResult.query.get_or_404(result_id)
        if test_result.test_run_id != run_id:
            return {'error': 'Test result not found in the specified test run'}, 404
        return {'id': test_result.id, 'status': test_result.status, 'output': test_result.output}

    def put(self, project_id, run_id, result_id):
        args = test_result_parser.parse_args()
        test_result = TestResult.query.get_or_404(result_id)
        if test_result.test_run_id != run_id:
            return {'error': 'Test result not found in the specified test run'}, 404
        test_result.status = args['status']
        test_result.output = args['output']
        db.session.commit()
        return {'id': test_result.id, 'status': test_result.status, 'output': test_result.output}

class TestResultListResource(Resource):
    def get(self, project_id, run_id):
        test_results = TestResult.query.filter_by(test_run_id=run_id).all()
        return [{'id': test_result.id, 'status': test_result.status, 'output': test_result.output} for test_result in test_results]

    def post(self, project_id, run_id):
        args = test_result_parser.parse_args()
        test_result = TestResult(status=args['status'], output=args['output'], test_run_id=run_id)
        db.session.add(test_result)
        db.session.commit()
        return {'id': test_result.id, 'status': test_result.status, 'output': test_result.output}


