from db import db
from sqlalchemy.orm import validates


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

    @validates('student_id')
    def validate_id(self, key, student_id):
        if not student_id:
            raise AssertionError('No Class id provided')
        # enrolls = EnrollModel.query.filter(
        #     EnrollModel.student_id == student_id).all()
        return student_id

    @validates('class_id')
    def validate_id(self, key, class_id):
        if not class_id:
            raise AssertionError('No Class id provided')
        return class_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def deactive(cls, student_id, class_id):
        enroll = cls.get_by_student_and_class(
            student_id=student_id, class_id=class_id)
        if enroll is None:
            raise AssertionError('Student does not enroll this class')
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
