# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_htmlmin import HTMLMIN
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from passlib.context import CryptContext

from .manage_webpack import FlaskManageWebpack

csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cache = Cache()
debug_toolbar = DebugToolbarExtension()
htmlmin = HTMLMIN()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
mail = Mail()
manage_webpack = FlaskManageWebpack()
