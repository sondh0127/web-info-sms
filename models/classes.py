from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from db import db
from flask_jwt_extended import get_jwt_claims
from models.account import AccountModel
from sqlalchemy.ext.associationproxy import association_proxy


class EnrollModel(db.Model):
    __tablename__ = 'enrolls'
    student_id = db.Column(db.Integer, db.ForeignKey(
        'accounts.id'),  primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey(
        'classes.id'),  primary_key=True)
    isRemoved = db.Column(db.Boolean, default=False)

    student = db.relationship('AccountModel', backref="enrolls")
    classes = db.relationship('ClassModel', backref="enrolls")

    def __init__(self, student_id, class_id):
        self.student_id = student_id
        self.class_id = class_id

    @validates('class_id')
    def validate_id(self, key, id):
        if not id:
            raise AssertionError('No Class id provided')

        enrolls = EnrollModel.query.filter(EnrollModel.class_id == id).all()
        student_ids = [e.student_id for e in enrolls]
        print(student_ids)
        # student_id = get_jwt_claims()['id']
        # if student_id in student_ids:
        #     raise AssertionError('Cannot register this class')
        return id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def deactive(cls, student_id, class_id):
        enroll = cls.get_by_student_and_class(
            student_id=student_id, class_id=class_id)
        if enroll.isRemoved:
            raise AssertionError('Enroll already deactived')
        enroll.isRemoved = True
        db.session.commit()
        return enroll

    @classmethod
    def get_by_student_and_class(cls, student_id, class_id):
        return cls.query.filter_by(
            student_id=student_id, class_id=class_id).first()

    @classmethod
    def get_by_student(cls, id):
        return EnrollModel.query.filter(
            EnrollModel.student_id == id, EnrollModel.isRemoved == False).all()

    @classmethod
    def get_by_class(cls, id):
        return EnrollModel.query.filter(
            EnrollModel.class_id == id, EnrollModel.isRemoved == False).all()

    # enrolls = db.Table(
    #     'enrolls',
    #     db.Column('student_id', db.Integer, db.ForeignKey(
    #         'accounts.id'), primary_key=True),
    #     db.Column('class_id', db.Integer, db.ForeignKey(
    #         'classes.id'), primary_key=True),
    #     db.Column('isRemoved', db.Boolean, default=False)
    # )


class ClassModel(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    student_limit = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.Enum('active', 'deleted', name='class_status'), default='active')
    # students = db.relationship('AccountModel', secondary=enrolls,
    #                            lazy='subquery', backref=db.backref('classes', lazy=True))
    tutor_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

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

    def __init__(self, name, student_limit):
        self.name = name
        self.student_limit = student_limit
        self.tutor_id = get_jwt_claims()['id']

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()

    def getStudents(self):
        enrolls = EnrollModel.get_by_class(self.id)
        return [s.student.name for s in enrolls]

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'student_limit': self.student_limit,
            'status': self.status,
            'tutor_id': self.tutor_id,
            'student_num': len(self.getStudents())
        }

    def get_students(self):
        return self.students

    def isAvailable(self):
        return len(self.students) < self.student_limit

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
    # @classmethod
    # def find_by_id(cls, _id):
    #     return cls.query.filter_by(id=_id).first()


ClassModel.students = association_proxy("enrolls", "student")
AccountModel.classes = association_proxy("enrolls", "classes")
