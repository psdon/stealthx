from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from stealthx.library.helper import auth_required
from stealthx.watcher import register_watchers
from .forms import AccountSettingsForm, ChangePasswordForm, PersonalInformationForm
from .services import update_account_service, change_password_service, personal_information_service

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.before_request
@auth_required
def _before():
    pass


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/dashboard/")
def dashboard():
    return render_template("account/dashboard/index.html")


@bp.route("/settings/", methods=["GET", "POST"])
def settings():
    form = AccountSettingsForm()
    if form.validate_on_submit():
        flag = update_account_service(username=form.username.data, email=form.email.data)

        if flag == "nothing_to_change":
            flash("Nothing changed!", "success")
            return redirect(url_for('account.settings'))

        if flag:
            flash("You have saved it successfully!", "success")
            return redirect(url_for('account.settings'))
        else:
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.settings'))

    else:
        if not form.username.data:
            form.username.data = current_user.username

        if not form.email.data:
            form.email.data = current_user.email

    return render_template("account/settings/index.html", form=form)


@bp.route("/change-password/", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        commit_success = change_password_service(form.new_password.data)

        if commit_success:
            flash("You have changed your password successfully!", "success")
            return redirect(url_for('account.settings'))
        else:
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.settings'))

    return render_template("account/change_password/index.html", form=form)


@bp.route("/personal-information/", methods=["GET", "POST"])
def personal_information():
    form = PersonalInformationForm()
    if form.validate_on_submit():
        commit_success = personal_information_service(form)

        if commit_success:
            flash("You have saved it successfully", "success")
        else:
            flash("Server error occurred. Please try again later", "warning")

        return redirect(url_for('account.personal_information'))
    else:
        try:
            if current_user.personal_info:
                data = {
                    "first_name": current_user.personal_info.first_name,
                    "middle_name": current_user.personal_info.middle_name,
                    "last_name": current_user.personal_info.last_name,
                    "mobile_number": current_user.personal_info.mobile_number,
                    "address_1": current_user.personal_info.address_1,
                    "address_2": current_user.personal_info.address_2,
                    "region": current_user.personal_info.region,
                    "city": current_user.personal_info.city,
                    "zip_code": current_user.personal_info.zip_code,
                    "country": current_user.personal_info.country,
                }
                form = PersonalInformationForm(**data)
        except AttributeError:
            pass

    return render_template("account/personal_information/index.html", form=form)
