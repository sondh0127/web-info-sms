from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import re


class AccountModel(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(
        db.Enum('tutor', 'student', 'admin', name='user_roles'), default='student')

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.set_password(password)
        self.role = role

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise AssertionError('No Account name provided')

        if len(name) < 3 or len(name) > 50:
            raise AssertionError(
                'Account name must be between 3 and 50 characters')
        return name

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No Account email provided')

        if AccountModel.query.filter(AccountModel.email == email).first():
            raise AssertionError('Account email is already in use')

        if len(email) < 3 or len(email) > 255:
            raise AssertionError(
                'Account email must be between 3 and 255 characters')
        return email

    def set_password(self, password):
        if not password:
            raise AssertionError('Password not provided')

        if re.match('.*\s.*', password):
            raise AssertionError(
                'Password can not have space')

        if not re.match('.*[0-9].*', password):
            raise AssertionError(
                'Password must contain 1 number')

        if len(password) < 5 or len(password) > 10:
            raise AssertionError(
                'Account password must be between 5 and 10 characters')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
