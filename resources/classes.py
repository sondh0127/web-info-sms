from flask_restful import Resource, reqparse
from helper.authorization import tutor_required
from models.classes import ClassModel, EnrollModel
from flask_jwt_extended import get_jwt_claims


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

    @tutor_required
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

    @tutor_required
    def put(self, name):
        data = Class.parser.parse_args()
        try:
            my_class = ClassModel.find_by_name_with_tutor(name)
            # if class does not exist, create new class with given name
            if my_class is None:
                my_class = ClassModel(name, data['student_limit'])
            else:
                if my_class.isDeleted():
                    return {
                        'message': 'Can not change deactived class'
                    }
                if name != data['name']:
                    my_class.name = data['name']
                my_class.student_limit = data['student_limit']
            my_class.save_to_db()
            return my_class.json(), 201

        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400

    @tutor_required
    def delete(self, name):
        my_class = ClassModel.find_by_name_with_tutor(name)
        if my_class:
            my_class.markDelete()
            return {'message': 'Classes deleted'}
        return {'message': 'Class not found or the class is not your own !'}

    @tutor_required
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
    @tutor_required
    def get(self):
        tutor = get_jwt_claims()['id']
        classes = ClassModel.query.filter_by(tutor_id=tutor).all()
        if classes:
            return [c.json() for c in classes]
        return {'message': 'No classes created'}, 404


class RemoveStudent(Resource):
    @tutor_required
    def delete(self, name, student_id):
        my_id = get_jwt_claims()['id']
        try:
            my_class = ClassModel.find_by_name_with_tutor(name)
            if my_class:
                enroll = EnrollModel.deactive(student_id, my_class.id)
                if enroll:
                    return {
                        'message': 'Remove student {} successfully!'.format(student_id),
                        'isRemove': enroll.isRemoved
                    }, 201
                return {'message: Student does not enroll the or'}
            return {'message': 'Class not found or the class is not your own !'}
        except AssertionError as exception_message:
            return {'message': 'Error: {}.'.format(exception_message)}, 400
