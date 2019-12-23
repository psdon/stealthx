# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template
from flask_talisman import Talisman
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from stealthx import account, auth, commands, models, public, settings
from stealthx.extensions import (
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    htmlmin,
    login_manager,
    mail,
    manage_webpack,
    migrate,
)

csp = {
    "default-src": "'self'",
    "script-src": "'self'",
    "connect-src": ["'self'", "https://vimeo.com"],
    "img-src": "'self'",
    "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    "font-src": "https://fonts.gstatic.com",
    "media-src": "https://player.vimeo.com",
    "frame-src": "https://player.vimeo.com",
    "base-uri": "'self'",
    "object-src": "'none'",
}


def create_app(testing=False, config_object=None):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param testing: Testing config object.
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])

    if testing:
        app.config.from_object(settings.TestingConfig)
    elif config_object:
        app.config.from_object(config_object)
    elif settings.BaseConfig.ENV == "development":
        app.config.from_object(settings.DevConfig)
    elif settings.BaseConfig.ENV == "production":
        app.config.from_object(settings.ProdConfig)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_not_supported_browser(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    htmlmin.init_app(app)
    mail.init_app(app)
    manage_webpack.init_app(app)

    if app.config["ENV"] == "production":
        Talisman(
            app,
            content_security_policy=csp,
            content_security_policy_nonce_in=["script-src"],
        )

        # sentry_sdk.init(
        #     dsn="https://cbf789f8b12f4d5b951ed0a52c6eea11@sentry.io/1863805",
        #     integrations=[FlaskIntegration()]
        # )

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.bp)
    app.register_blueprint(auth.views.bp)
    app.register_blueprint(account.views.bp)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)

        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)

    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.init)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_not_supported_browser(app):
    @app.route("/not-supported")
    def route():
        return render_template("not_supported.html")
