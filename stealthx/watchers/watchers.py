from datetime import datetime as dt

from flask import flash, redirect, url_for
from flask_login import current_user

from stealthx.daos import current_user_dao


def subscription_watcher():
    if current_user.subscription.type.name == "free":
        return None

    if current_user.subscription.expiration <= dt.utcnow():
        current_user_dao.set_subscription_free()

        if not current_user_dao.commit():
            flash("Server error occurred. Please try again later.")

        return redirect(url_for('account.subscription'))


def is_student_watcher():
    if current_user.subscription.type.name == "free":
        return None

    if not current_user.subscription.is_student:
        return None

    if current_user.subscription.is_student_renewal <= dt.utcnow():
        current_user_dao.set_is_student(False)

        if not current_user_dao.commit():
            flash("Server error occurred. Please try again later.")
