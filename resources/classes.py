from flask_restful import Resource, reqparse
from helper.authorization import requires_access_role
from models.classes import ClassModel
from flask_jwt_extended import get_jwt_claims, jwt_required


class Class(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'student_limit',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )

    @requires_access_role('tutor')
    def post(self, name):
        data = Class.parser.parse_args()
        try:
            new_class = ClassModel(
                name=name,
                student_limit=data['student_limit']
            )
            new_class.save_to_db()
            return {
                'message': 'Class {} was created'.format(data['name'])
            }, 201
        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400

    @requires_access_role('tutor')
    def put(self, name):
        data = Class.parser.parse_args()
        try:
            my_class = ClassModel.find_by_name_with_tutor(name)
            # if class does not exist, create new class with given name
            if my_class is None:
                raise AssertionError(
                    'Class not found or the class is not your own')
            else:
                if my_class.isDeleted():
                    raise AssertionError('Can not change deactived class')
                if data['student_limit'] < len(my_class.getStudents()):
                    raise AssertionError(
                        'Number of student limit can not less current enroll student')
                if name != data['name']:
                    my_class.name = data['name']
                my_class.student_limit = data['student_limit']
            my_class.save_to_db()
            return my_class.json(), 201

        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400

    @requires_access_role('tutor')
    def delete(self, name):
        my_class = ClassModel.find_by_name_with_tutor(name)
        if my_class:
            my_class.markDelete()
            return {'message': 'Classes deleted'}
        return {'message': 'Class not found or the class is not your own.'}

    @requires_access_role('tutor')
    # get student list of a given class name
    def get(self, name):
        my_class = ClassModel.find_by_name_with_tutor(name)
        if my_class:
            return {
                'students': [student.json() for student in my_class.students]
            }
        return {'message': 'Class not found or the class is not your own !'}


class ClassList(Resource):
     # get all list of classes
    @jwt_required
    def get(self):
        if get_jwt_claims()['role'] == 'tutor':
            tutor = get_jwt_claims()['id']
            classes = ClassModel.query.filter_by(tutor_id=tutor).all()
            if classes:
                return [c.json() for c in classes]
            return {'message': 'No classes created'}, 404
        else:
            # return active classes name for student
            classes = ClassModel.query.filter_by(status='active').all()
            if classes:
                return [c.name for c in classes]
            return {'message': 'No classes available'}, 404
