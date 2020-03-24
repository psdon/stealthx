from flask import current_app
from sentry_sdk import capture_exception

from stealthx.extensions import db


class BaseDAO:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def add_commit_obj(obj):
        db.session.add(obj)

    @staticmethod
    def commit():
        try:
            db.session.commit()
            return True
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            capture_exception(error)
