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
    DEBUG_TB_ENABLED = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEBPACK_MANIFEST_PATH = "webpack/manifest.json"


class DevConfig(BaseConfig):
    MINIFY_HTML = False


class ProdConfig(BaseConfig):
    MINIFY_HTML = True
    SEND_FILE_MAX_AGE_DEFAULT = 31556926
