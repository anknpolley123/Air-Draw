from flask import session, redirect, url_for, request, flash
from functools import wraps
from database import DrawingDatabase


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def optional_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            db = DrawingDatabase()
            try:
                kwargs['user'] = db.get_user_by_id(session['user_id'])
            finally:
                db.close()
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    if 'user_id' not in session:
        return None

    db = DrawingDatabase()
    try:
        return db.get_user_by_id(session['user_id'])
    finally:
        db.close()


def get_api_key():
    if 'api_key' in session:
        return session['api_key']
    return None