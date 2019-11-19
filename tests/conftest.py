# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import logging

import pytest
from webtest import TestApp

from stealthx.app import create_app
from stealthx.database import db as _db

from .factories import UserFactory


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app(testing=True)
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    """Create Webtest app."""
    return app.test_client()


@pytest.fixture
def web_client(app):
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """Create user for the tests."""
    user = UserFactory(password="a-long-password-987")
    db.session.commit()
    return user
