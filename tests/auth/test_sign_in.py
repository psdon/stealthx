from flask import url_for


class TestSignIn:
    """Login."""

    def test_can_sign_in_returns_200(self, user, web_client):
        """Sign in successful."""
        res = web_client.get("/sign-in").follow()

        form = res.form
        form["username_or_email"] = user.username
        form["password"] = "a-long-password-987"
        # Submits
        res = form.submit().maybe_follow()
        assert res.status_code == 200
        assert "<h1>This is a restricted area</h1>" in res

    def test_sign_in_not_email_confirm(self, user, web_client):
        user.email_confirmed = False
        res = web_client.get("/sign-in").follow()

        form = res.form
        form["username_or_email"] = user.username
        form["password"] = "a-long-password-987"

        # Submits
        res = form.submit().maybe_follow()
        assert res.status_code == 200
        assert "We have sent you an email, please check your email and confirm." in res

    def test_redirect_home_in_sign_out(self, user, web_client):
        """Redirect to home page when sign out"""
        res = web_client.get("/sign-in").follow()
        # Fills out login form in navbar
        form = res.form
        form["username_or_email"] = user.username
        form["password"] = "a-long-password-987"

        # Submits
        form.submit().maybe_follow()
        res = web_client.get(url_for("auth.sign_out")).maybe_follow()

        # Redirected to Home
        assert 'data-view="home"' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, web_client):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = web_client.get("/sign-in").follow()

        # Fills out login form, password incorrect
        form = res.form
        form["username_or_email"] = user.username
        form["password"] = "wrong"
        # Submits
        res = form.submit()

        # sees error
        assert "Incorrect username or password" in res

    def test_sees_error_message_if_username_is_incorrect(self, db, web_client):
        """Show error if username is incorrect."""
        # Goes to homepage
        res = web_client.get("/sign-in").follow()

        # Fills out login form, password incorrect
        form = res.form
        form["username_or_email"] = "wrong"
        form["password"] = "wrong"
        # Submits
        res = form.submit()

        # sees error
        assert "Incorrect username or password" in res

