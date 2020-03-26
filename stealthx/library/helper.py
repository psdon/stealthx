import uuid

from flask import current_app, session, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps

from stealthx.daos import current_user_dao


def is_url_safe(url):
    for r in current_app.url_map._rules:
        if r.rule == next:
            return url
    return False


def login(user_obj):
    login_user(user_obj)
    token = uuid.uuid4().hex
    session['session_token'] = token
    current_user_dao.set_session_token(token)

    if not current_user_dao.commit():
        flash("Server error occurred. Please try again later.")
        return None

    return True


def logout():
    logout_user()
    if 'session_token' in session:
        session.pop('session_token')


def auth_required(func):
    @login_required
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_authenticated and session['session_token'] != current_user.session_token:
            logout()
            flash("You have been sign-out. You can only sign-in in one device.", "warning")
            return redirect(url_for('auth.sign_in'))
        return func(*args, **kwargs)
    return decorated_view
