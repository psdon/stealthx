from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from stealthx.library.helper import auth_required
from stealthx.watchers.watcher import register_watchers
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


@bp.route("/profile/")
def profile():
    return render_template("account/profile/index.html")


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

    if not form.errors:
        form.username.data = current_user.username
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
            return redirect(url_for('account.personal_information'))
        else:
            flash("Server error occurred. Please try again later", "warning")

    if not form.errors:
        if current_user.personal_info:
            form.first_name.data = current_user.personal_info.first_name
            form.middle_name.data = current_user.personal_info.middle_name
            form.last_name.data = current_user.personal_info.last_name
            form.mobile_number.data = current_user.personal_info.mobile_number
            form.address_1.data = current_user.personal_info.address_1
            form.address_2.data = current_user.personal_info.address_2
            form.region.data = current_user.personal_info.region
            form.city.data = current_user.personal_info.city
            form.zip_code.data = current_user.personal_info.zip_code
            form.country.data = current_user.personal_info.country

    return render_template("account/personal_information/index.html", form=form)


@bp.route("/subscription")
def subscription():
    return render_template("account/subscription/index.html")
