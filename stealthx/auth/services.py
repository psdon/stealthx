# Business Logic

from flask import flash

from stealthx.daos import user_dao, current_user_dao
from .utils import send_confirm_email


def sign_up_service(username, email, password):
    user_dao.register_user(username=username, email=email, password=password)
    commit_success = user_dao.commit()

    if commit_success:
        send_confirm_email(email)
        flash("You have signed up successfully. Please check your email", "success")
        return True
    else:
        flash("Oops, an error occurred. Please try again later.", "warning")


def confirm_your_email_service(email):
    current_user_dao.change_email(email=email, set_confirm=None)
    commit_success = current_user_dao.commit()

    if not commit_success:
        flash("Oops, an error occurred. Please try again later.", "warning")


def confirm_email_service(email):
    user_obj = user_dao.get_user_by_email_or_404(email)

    if user_obj.email_confirmed:
        flash("Email already confirmed. Please sign in.", "success")
    else:
        user_dao.set_email_confirmed(email=email)
        commit_success = user_dao.commit()

        if commit_success:
            flash("You have successfully confirmed your email. You can now sign in.", "success")
        else:
            flash("Oops, an error occurred. Please try again later.", "warning")


def reset_password_service(email, password):
    """
    :param email:
    :param password:
    :return: True, if successfully reset the password
    """
    user_exist = user_dao.reset_password(email, password)
    if user_exist:
        commit_success = user_dao.commit()
        if commit_success:
            flash("You have successfully reset your password. You can now sign in.", "success")
            return True
    else:
        flash("Oops, an error occurred. Please try again later.", "warning")
