from functools import wraps
from models.account import AccountModel
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        role = get_jwt_claims()['role']
        if role != 'admin':
            raise AssertionError('Admins only!')
        else:
            return fn(*args, **kwargs)
    return wrapper


def tutor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        role = get_jwt_claims()['role']
        if role != 'tutor':
            # return jsonify(message='Tutors only!'), 403
            raise AssertionError('Tutors only!')
        else:
            return fn(*args, **kwargs)
    return wrapper


def requires_access_role(access_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt_claims()['role']
            if role != access_role:
                raise AssertionError(
                    '{} only!'.format(access_role.capitalize()))
            else:
                return fn(*args, **kwargs)
        return wrapper
    return decorator
