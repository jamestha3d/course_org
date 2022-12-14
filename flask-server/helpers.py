from flask import jsonify, session, redirect
from functools import wraps


def error(message, number):
    return {
        'message': message,
        'status': number
    }

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

