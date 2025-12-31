from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required
from flask import jsonify
from functools import wraps

def role_required(*allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", "").lower()  

            allowed = [r.lower() for r in allowed_roles]

            if role not in allowed:
                return {"message": "Forbidden"}, 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper

