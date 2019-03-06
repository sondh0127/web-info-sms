from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, get_jwt_claims

from models.account import AccountModel
from helper.authorization import admin_required, tutor_required

from resources.account import UserRegistration, UserLogin, TutorRegistration, StudentRegistration
from resources.classes import Class, ClassList, RemoveStudent
from resources.students import Enroll, StudentEnroll


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@127.0.0.1:3306/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
app.config.from_object('config.BaseConfig')
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        'id': user.id,
        'role': user.role
    }


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


api.add_resource(TutorRegistration, '/tutor/register')
api.add_resource(StudentRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Class, '/class/<string:name>')
api.add_resource(ClassList, '/classes')
api.add_resource(RemoveStudent, '/class/<string:name>/<int:student_id>')
api.add_resource(Enroll, '/enroll/<string:name>')
api.add_resource(StudentEnroll, '/enrolls')


@app.route('/test')
def test():
    return jsonify({
        'username': app.config['ADMIN']['username'],
        'password': app.config['ADMIN']['password']
    })


@app.route('/protect')
@jwt_required
# @admin_required
def method_name():
    claims = get_jwt_claims()
    return jsonify({
        'identity': get_jwt_identity(),
        'role': claims['role']
    })


if __name__ == '__main__':
    # app.run(port=5000)
    from db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=5000, debug=True)
