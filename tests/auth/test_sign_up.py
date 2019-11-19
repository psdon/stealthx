from stealthx.models import  User
from flask import  url_for
from tests.factories import UserFactory


class TestSignUp:
    """Register a user."""

    def test_can_sign_up(self, user, web_client):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = web_client.get("/sign-up")

        # Fills out the form
        form = res.form
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret-1234567890"
        form["confirm"] = "secret-1234567890"
        
        # Submits
        res = form.submit().maybe_follow()
        assert res.status_code == 200
        assert "You have signed up successfully. Please check your email" in res

        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, web_client):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = web_client.get(url_for("auth.sign_up"))

        # Fills out form, but passwords don't match
        form = res.form
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret1234567890"
        form["confirm"] = "secrets"

        # Submits
        res = form.submit()

        # sees error message
        assert "Password does not match" in res

    def test_sees_error_message_if_password_is_not_secured(self, user, web_client):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()

        # Goes to sign up page
        res = web_client.get(url_for("auth.sign_up"))

        # Fills out form, but username is already registered
        form = res.form
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "short"
        form["confirm"] = "short"

        # Submits
        res = form.submit()

        # sees error
        assert "Field must be at least 8 characters long." in res

    def test_sees_error_message_if_user_already_registered(self, user, web_client):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()

        # Goes to sign up page
        res = web_client.get(url_for("auth.sign_up"))

        # Fills out form, but username is already registered
        form = res.form
        form["username"] = user.username
        form["email"] = user.email
        form["password"] = "secret"
        form["confirm"] = "secret"

        # Submits
        res = form.submit()

        # sees error
        assert "This username is taken" in res
        assert "This email is already registered" in res
