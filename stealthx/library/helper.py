import uuid

from flask import current_app, session, flash
from flask_login import login_user, logout_user

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
