# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from stealthx.database import (
    Column,
    Model,
    SurrogatePK,
    db,
)
from stealthx.extensions import login_manager, pwd_context


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id))


login_manager.login_view = "auth.sign_in"
login_manager.login_message = "Please sign in to access this page"
login_manager.login_message_category = "warning"


class Role(db.Model):
    """A role for a user."""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("User", backref="role")

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Role({name})>".format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(30), unique=True, nullable=False)
    email = Column(db.String(45), unique=True, nullable=False)
    email_confirmed = Column(db.Boolean, default=False, nullable=False)
    email_confirmed_at = Column(db.DateTime, nullable=True)
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)

    def __init__(self, username, email, password=None, email_confirmed=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, email_confirmed=None, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

        if email_confirmed:
            self.email_confirmed_at = dt.datetime.utcnow()

    def set_password(self, password):
        """Set password."""
        self.password = pwd_context.hash(password)

    def check_password(self, value):
        """Check password."""
        return pwd_context.verify(value, self.password)

    @property
    def is_active(self):
        return True if self.active else False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def full_name(self):
        """Full user name."""
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)
