# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()


class BaseConfig:
    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"
    SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
    SECRET_KEY = env.str("SECRET_KEY")
    PASSWORD_SALT_KEY = env.str("PASSWORD_SALT_KEY")
    DEBUG_TB_ENABLED = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    # mail settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = "connect.stealthx@gmail.com"
    MAIL_PASSWORD = "P9xEo2NW"

    # mail accounts
    MAIL_DEFAULT_SENDER = "connect.stealthx@gmail.com"


class DevConfig(BaseConfig):
    MINIFY_HTML = False


class ProdConfig(BaseConfig):
    MINIFY_HTML = True
    SEND_FILE_MAX_AGE_DEFAULT = 31556926

    # To get the right value:
    # SHOW GLOBAL VARIABLES LIKE "wait_timeout";
    # SQLALCHEMY_POOL_RECYCLE = <wait_timeout> - 1
    SQLALCHEMY_POOL_RECYCLE = 299  # PythonAnywhere Specific
