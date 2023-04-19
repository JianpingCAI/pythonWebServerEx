from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    test_suites = db.relationship('TestSuite', backref='project', lazy=True)
    test_runs = db.relationship('TestRun', backref='project', lazy=True)

class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    test_cases = db.relationship('TestCase', backref='test_suite', lazy=True)

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'), nullable=False)

class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    test_results = db.relationship('TestResult', backref='test_run', lazy=True)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False)
    output = db.Column(db.Text, nullable=True)

    test_run_id = db.Column(db.Integer, db.ForeignKey('test_run.id'), nullable=False)
    test_case_id = db.Column(db.Integer, db.ForeignKey('test_case.id'), nullable=False)
