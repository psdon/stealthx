# -*- coding: utf-8 -*-
"""Test forms."""

from stealthx.auth.forms import SignInForm
from stealthx.auth.forms import SignUpForm


class TestRegisterForm:
    """Register form."""

    def test_validate_user_already_registered(self, user):
        """Enter username that is already registered."""
        form = SignUpForm(
            username=user.username,
            email="foo@bar.com",
            password="example",
            confirm="example",
        )

        assert form.validate() is False
        assert "This username is taken" in form.username.errors

    def test_validate_email_already_registered(self, user):
        """Enter email that is already registered."""
        form = SignUpForm(
            username="unique", email=user.email, password="example", confirm="example"
        )

        assert form.validate() is False
        assert "This email is already registered" in form.email.errors

    def test_validate_success(self, db):
        """Register with success."""
        form = SignUpForm(
            username="newusername",
            email="new@test.test",
            password="a-long-valid-password",
            confirm="a-long-valid-password",
        )
        assert form.validate() is True


class TestLoginForm:
    """Login form."""

    def test_validate_success(self, user):
        """Login successful."""
        user.set_password("example")
        user.save()
        form = SignInForm(username_or_email=user.username, password="example")
        assert form.validate() is True
        assert form.username_or_email == user.username or user.email

    def test_validate_no_username(self, db):
        """Unknown username."""
        form = SignInForm(password="example")
        assert form.validate() is False
        assert "This field is required." in form.username_or_email.errors
        assert form.username_or_email.data is None

