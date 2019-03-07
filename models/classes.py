from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from db import db
from flask_jwt_extended import get_jwt_claims
from models.account import AccountModel
from models.enroll import EnrollModel
from sqlalchemy.ext.associationproxy import association_proxy


class ClassModel(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    student_limit = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum('active', 'deleted', name='class_status'), default='active')
    tutor_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __init__(self, name, student_limit):
        self.name = name
        self.student_limit = student_limit
        self.tutor_id = get_jwt_claims()['id']

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('No Class name provided')

        if ClassModel.query.filter(ClassModel.name == name).first():
            raise AssertionError('Class name is already in use')

        if len(name) < 3 or len(name) > 50:
            raise AssertionError(
                'Class name must be between 3 and 50 characters')
        return name

    @validates('student_limit')
    def validate_student_limit(self, key, student_limit):
        if student_limit < 1 or student_limit > 15:
            raise AssertionError(
                'The number of students in the class must be be between 1-15')
        return student_limit

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def getStudents(self):
        enrolls = EnrollModel.get_by_class(self.id)
        return [s.student.name for s in enrolls]

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_limit': self.student_limit,
            'status': self.status,
            'student_num': len(self.getStudents())
        }

    def isAvailable(self):
        return len(self.getStudents()) < self.student_limit and self.status == 'active'

    def isDeleted(self):
        return self.status == 'deleted'

    def markDelete(self):
        self.status = 'deleted'
        db.session.commit()

    @classmethod
    def find_by_name_with_tutor(cls, name):
        return cls.query.filter_by(name=name, tutor_id=get_jwt_claims()['id']).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


ClassModel.students = association_proxy("enrolls", "student")
AccountModel.classes = association_proxy("enrolls", "classes")
