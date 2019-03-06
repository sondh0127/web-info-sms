from flask_restful import Resource, reqparse
from helper.authorization import requires_access_role
from models.classes import ClassModel, EnrollModel
from models.account import AccountModel
from flask_jwt_extended import get_jwt_claims, get_jwt_identity
from flask import jsonify


class Enroll(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @requires_access_role('student')
    def post(self, name):
        data = Enroll.parser.parse_args()
        try:
            enroll_class = ClassModel.find_by_name(name)
            student_id = get_jwt_claims()['id']
            if enroll_class:
                if enroll_class.isAvailable():
                    enroll = EnrollModel(student_id, enroll_class.id)
                    enroll.save_to_db()
                    return {
                        'message': 'Enroll {} successfully!'.format(data['name']),
                        'students': [c.id for c in enroll_class.students]
                    }, 201
                return {'message': 'No slot available or you cannot register this class'}
            return {'message': 'Class not found!'}

        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400

    @requires_access_role('student')
    # change enroll record to isRemoved = True
    def put(self, name):
        data = Enroll.parser.parse_args()
        try:
            enroll_class = ClassModel.find_by_name(name)
            student_id = get_jwt_claims()['id']
            if enroll_class:
                enroll = EnrollModel.deactive(
                    student_id.id, enroll_class.id)
                return {
                    'message': 'Enroll {} successfully!'.format(data['name']),
                    'students': enroll.isRemoved
                }, 201
            return {'message': 'Class not found!'}

        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400


class StudentEnroll(Resource):
    @requires_access_role('student')
    # get the enroll class of the students
    def get(self):
        user = AccountModel.find_by_id(get_jwt_claims()['id'])
        classes = [c.name for c in user.classes]
        return {'classes': classes}
