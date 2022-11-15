# Business Logic

from flask_login import current_user

from stealthx.auth.utils import send_confirm_email
from stealthx.daos import current_user_dao, personal_info_dao


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


def personal_information_service(form):
    data = {
        "first_name": form.first_name.data,
        "middle_name": form.middle_name.data,
        "last_name": form.last_name.data,
        "mobile_number": form.mobile_number.data,
        "address_1": form.address_1.data,
        "address_2": form.address_2.data,
        "region": form.region.data,
        "city": form.city.data,
        "zip_code": form.zip_code.data,
        "country": form.country.data,
    }

    if current_user.personal_info:
        personal_info_dao.update_personal_info(user_id=current_user.id, **data)
        commit_success = personal_info_dao.commit()
        return commit_success

    personal_info_dao.init_personal_info(user_id=current_user.id, **data)
    commit_success = personal_info_dao.commit()

    return commit_success
