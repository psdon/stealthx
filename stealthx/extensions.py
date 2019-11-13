# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_htmlmin import HTMLMIN
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_webpack import Webpack
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from passlib.context import CryptContext
from flask_static_digest import FlaskStaticDigest

csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
cache = Cache()
debug_toolbar = DebugToolbarExtension()
htmlmin = HTMLMIN()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
mail = Mail()
flask_static_digest = FlaskStaticDigest()