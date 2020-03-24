# Business Logic

from flask_login import current_user

from stealthx.auth.utils import send_confirm_email
from stealthx.daos import current_user_dao


def update_account_service(username, email):
    """
    :param username:
    :param email:
    :return: "nothing_to_change"
    :return: True, if success
    """
    username_changed = current_user.username != username
    email_changed = current_user.email != email

    if not (username_changed or email_changed):
        return "nothing_to_change"

    if username_changed:
        current_user_dao.change_username(username)

    if email_changed:
        current_user_dao.change_email(email)

    if username_changed or email_changed:
        commit_success = current_user_dao.commit()

        if email_changed and commit_success:
            send_confirm_email(email)

        return commit_success


def change_password_service(password):
    current_user_dao.change_password(password)
    commit_success = current_user_dao.commit()
    return commit_success
