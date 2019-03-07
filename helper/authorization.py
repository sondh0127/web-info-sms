from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims


def requires_access_role(access_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt_claims()['role']
            if role != access_role:
                return '{} only!'.format(access_role.capitalize())
            else:
                return fn(*args, **kwargs)
        return wrapper
    return decorator
