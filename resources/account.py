from models.account import AccountModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt_claims)
from flask import current_app
from helper.authorization import admin_required, tutor_required


class UserRegistration(Resource):
    def __init__(self, role):
        self.role = role

    def post(self):
        # print(self.role)
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name',
            type=str,
            required=True,
            help="This field cannot be left blank!"
        )
        parser.add_argument(
            'email',
            type=str,
            required=True,
            help="This field cannot be left blank!"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="This field cannot be left blank!"
        )
        data = parser.parse_args()
        try:
            new_user = AccountModel(
                name=data['name'],
                email=data['email'],
                password=data['password'],
                role=self.role
            )
            new_user.save_to_db()
            access_token = create_access_token(identity=new_user)
            return {
                'message': 'User {} was created'.format(data['email']),
                'access_token': access_token,
            }
        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'email',
            type=str,
            required=True,
            help="This field cannot be left blank!"
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help="This field cannot be left blank!"
        )
        data = parser.parse_args()
        # admin case
        usernameAdmin = current_app.config['ADMIN']['username']
        passwordAdmin = current_app.config['ADMIN']['password']
        if data['email'] == usernameAdmin:
            if data['password'] == passwordAdmin:
                user = AccountModel('Admin', usernameAdmin,
                                    passwordAdmin, 'admin')
                access_token = create_access_token(identity=user)
                return {
                    'message': 'Logged in as admin',
                    'access_token': access_token,
                }
        else:
            user = AccountModel.find_by_email(data['email'])
            if not user:
                return {'message': 'User {} doesn\'t exist'.format(data['email'])}

            if user.check_password(data['password']):
                access_token = create_access_token(identity=user)
                return {
                    'message': 'Logged in as {} ({})'.format(user.role, user.email),
                    'access_token': access_token,
                }
            return {'message': 'Wrong credentials'}


class TutorRegistration(UserRegistration):
    def __init__(self):
        super().__init__('tutor')

    @admin_required
    def post(self):
        return super().post()


class StudentRegistration(UserRegistration):
    def __init__(self):
        super().__init__('student')

    def post(self):
        return super().post()
